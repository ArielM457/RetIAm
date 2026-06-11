#!/usr/bin/env python
"""Ingesta de contenido de cursos (Fase 1 del modulo de cursos).

Construye el catalogo de cursos de RetAIM (courses -> sections -> lessons -> labs)
a partir de la API publica y gratuita de Microsoft Learn Catalog, y deja:

  1. Archivos markdown en synthetic-data/certifications/<cert>/...  (para indexar
     en Azure AI Search / Foundry IQ con infra/knowledge_base.sh).
  2. Un snapshot JSON por curso en synthetic-data/courses/<cert>.json.
  3. (opcional, con --push) el curso insertado/actualizado en Supabase.

Microsoft Learn cubre Azure y GitHub. AWS no esta en MS Learn, asi que se genera
desde una plantilla sintetica curada con citas a documentacion publica.

Uso:
    python infra/ingest_content.py                      # todos los certs, solo archivos
    python infra/ingest_content.py --certs AZ-900       # un cert
    python infra/ingest_content.py --push               # ademas sube a Supabase
    python infra/ingest_content.py --content --push     # + contenido COMPLETO legible (Markdown)
    python infra/ingest_content.py --rag --push         # + RAG del tutor (implica --content)
    python infra/ingest_content.py --insecure-ssl       # si tu red rompe la cadena TLS

Sin --content, content_md es el resumen oficial + cita de la fuente (rapido).
Con --content, se baja el texto COMPLETO de cada unidad de MS Learn y se guarda
como Markdown legible en content_md (lo que lee el estudiante). Con --rag, ademas
se trocea ese texto, se generan embeddings y se sube a pgvector para el tutor.
"""

from __future__ import annotations

import argparse
import http.client
import json
import os
import re
import ssl
import sys
import time
import urllib.request
from urllib.error import HTTPError, URLError
from pathlib import Path

CATALOG_URL = "https://learn.microsoft.com/api/catalog/?type=learningPaths,modules&locale=en-us"
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = REPO_ROOT / "synthetic-data"

# Mapeo curado certificacion -> learning paths de MS Learn + metadata.
# learning_paths: uids exactos verificados contra la API del catalogo.
# keyword_uid_prefix: descubrimiento extra de learning paths por prefijo de uid.
MS_LEARN_CERTS: dict[str, dict] = {
    "AZ-900": {
        "track": "azure",
        "provider": "Microsoft",
        "level": "basic",
        "title": "Microsoft Azure Fundamentals",
        "summary": "Fundamentos de nube, arquitectura, servicios y gobernanza de Azure.",
        "learning_paths": [
            "learn.wwl.microsoft-azure-fundamentals-describe-cloud-concepts",
            "learn.wwl.azure-fundamentals-describe-azure-architecture-services",
            "learn.wwl.describe-azure-management-governance",
        ],
        "keyword_uid_prefix": [],
    },
    "AZ-204": {
        "track": "azure",
        "provider": "Microsoft",
        "level": "intermediate",
        "title": "Developing Solutions for Microsoft Azure",
        "summary": "Desarrollo de soluciones cloud en Azure: compute, storage, seguridad e integracion.",
        "learning_paths": [
            "learn.wwl.create-azure-app-service-web-apps",
            "learn.wwl.implement-azure-functions",
            "learn.wwl.develop-solutions-that-use-blob-storage",
        ],
        "keyword_uid_prefix": [],
    },
    "GitHub Foundations": {
        "track": "github",
        "provider": "GitHub",
        "level": "basic",
        "title": "GitHub Foundations",
        "summary": "Colaboracion, flujo de pull requests, automatizacion con Actions y seguridad en GitHub.",
        "learning_paths": [
            "learn.github-foundations",
            "learn.github.github-administration-products-1",
        ],
        "keyword_uid_prefix": [],
    },
}

# Plantillas sinteticas curadas para certificaciones fuera de MS Learn (p.ej. AWS).
SYNTHETIC_CERTS: dict[str, dict] = {
    "AWS Cloud Practitioner": {
        "track": "aws",
        "provider": "Amazon",
        "level": "basic",
        "title": "AWS Certified Cloud Practitioner",
        "summary": "Fundamentos de la nube de AWS: valor, servicios core, seguridad y facturacion.",
        "sections": [
            {
                "title": "Conceptos de la nube de AWS",
                "summary": "Propuesta de valor de la nube y el modelo de responsabilidad compartida.",
                "lessons": [
                    {"title": "Que es la nube y la propuesta de valor de AWS", "minutes": 25,
                     "objectives": ["Explicar las 6 ventajas de la nube", "Reconocer la propuesta de valor de AWS"],
                     "source": {"title": "AWS Cloud Concepts", "url": "https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html"}},
                    {"title": "Modelo de responsabilidad compartida", "minutes": 20,
                     "objectives": ["Distinguir responsabilidades de AWS vs cliente"],
                     "source": {"title": "Shared Responsibility Model", "url": "https://aws.amazon.com/compliance/shared-responsibility-model/"}},
                ],
            },
            {
                "title": "Servicios core de AWS",
                "summary": "Compute, storage, redes y bases de datos principales.",
                "lessons": [
                    {"title": "Compute: EC2, Lambda y contenedores", "minutes": 30,
                     "objectives": ["Diferenciar EC2, Lambda y ECS/EKS"],
                     "source": {"title": "AWS Compute", "url": "https://docs.aws.amazon.com/whitepapers/latest/aws-overview/compute-services.html"}},
                    {"title": "Storage y bases de datos: S3, EBS, RDS, DynamoDB", "minutes": 30,
                     "objectives": ["Elegir el servicio de storage adecuado", "Reconocer casos de RDS vs DynamoDB"],
                     "source": {"title": "AWS Storage", "url": "https://docs.aws.amazon.com/whitepapers/latest/aws-overview/storage-services.html"}},
                ],
            },
            {
                "title": "Seguridad, identidad y facturacion",
                "summary": "IAM, seguridad gestionada y modelos de costos.",
                "lessons": [
                    {"title": "IAM y seguridad en AWS", "minutes": 25,
                     "objectives": ["Aplicar el principio de menor privilegio con IAM"],
                     "source": {"title": "AWS IAM", "url": "https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html"}},
                    {"title": "Precios, facturacion y soporte", "minutes": 20,
                     "objectives": ["Reconocer los modelos de precios de AWS"],
                     "source": {"title": "AWS Pricing", "url": "https://aws.amazon.com/pricing/"}},
                ],
            },
        ],
    },
}


def slugify(value: str, max_len: int = 60) -> str:
    value = re.sub(r"^learn\.", "", value)
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return (value[:max_len].strip("-") or "item")


def make_ssl_context(insecure: bool) -> ssl.SSLContext | None:
    if not insecure:
        return None
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch_catalog(ctx: ssl.SSLContext | None) -> tuple[dict, dict]:
    req = urllib.request.Request(CATALOG_URL, headers={"User-Agent": "retaim-ingest/1.0"})
    with urllib.request.urlopen(req, timeout=90, context=ctx) as response:
        data = json.load(response)
    lps_by_uid = {lp["uid"]: lp for lp in data.get("learningPaths", [])}
    mods_by_uid = {m["uid"]: m for m in data.get("modules", [])}
    return lps_by_uid, mods_by_uid


# --- Contenido completo: descarga de unidades, Markdown legible, troceo y RAG ---


def _http_get(url: str, ctx: ssl.SSLContext | None, timeout: int = 90, retries: int = 3) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 retaim"})
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
                return response.read().decode("utf-8", "replace")
        except KeyboardInterrupt:
            raise
        except HTTPError:
            raise
        except (TimeoutError, URLError, http.client.IncompleteRead, ssl.SSLError, ConnectionError) as exc:
            last_exc = exc
            if attempt == retries:
                break
            print(f"    reintento {attempt}/{retries - 1} para {url}")
            time.sleep(min(2 * attempt, 5))
    raise RuntimeError(f"no se pudo descargar {url}: {last_exc}") from last_exc


def _clean_unit_text(html: str) -> str:
    """Texto plano de la unidad (para los embeddings del RAG)."""
    match = re.search(r"<main[^>]*>(.*?)</main>", html, re.S)
    block = match.group(1) if match else html
    block = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", block, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", block)
    text = re.sub(r"\s+", " ", text).strip()
    # Quita el prefijo de navegacion ("... Completed N minutes ").
    text = re.sub(r"^.*?Completed\s+\d+\s+minutes?\s+", "", text, count=1)
    # Corta la cola de navegacion.
    text = re.split(r"(Next unit:|Having an issue|Module incomplete)", text)[0]
    return text.strip()


_TAIL_MARKERS = re.compile(
    r"(?:^|\n)\s*(?:#+\s*)?(?:Next unit:|Previous unit|Having an issue|Module incomplete|"
    r"Was this page helpful|Need help with this topic|Ask Learn|###?\s*Feedback)",
    re.I,
)
_DURATION_LINE = re.compile(r"^[*\-]?\s*\d+\s+minutes?\s*$", re.I)


def _clean_markdown(md: str) -> str:
    """Limpia el Markdown crudo de una unidad: quita breadcrumb, badges y cola de navegacion."""
    # Corta la cola de navegacion / feedback de MS Learn.
    md = _TAIL_MARKERS.split(md)[0]
    lines = md.split("\n")
    # Arranca desde el primer encabezado (salta breadcrumb y enlaces de navegacion).
    for i, line in enumerate(lines):
        if line.lstrip().startswith("#"):
            lines = lines[i:]
            break
    out: list[str] = []
    skip = {"Completed", "XP", "Next unit", "Previous unit", "edit"}
    for line in lines:
        stripped = line.strip()
        # Salta lineas vacias-decorativas, imagenes y badges de duracion/XP.
        if stripped in skip or stripped.startswith("![") or _DURATION_LINE.match(stripped):
            if not stripped:
                out.append("")
            continue
        if stripped in ("*", "-"):
            continue
        out.append(line)
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Quita reglas horizontales sobrantes al inicio/fin.
    text = re.sub(r"^(?:\s*---\s*)+", "", text)
    text = re.sub(r"(?:\s*---\s*)+$", "", text)
    return text.strip()


def _html_to_markdown(html: str) -> str:
    """Convierte el HTML de una unidad de MS Learn a Markdown legible.

    Usa beautifulsoup4 + markdownify si estan disponibles; si no, cae a texto plano.
    """
    try:
        from bs4 import BeautifulSoup
        from markdownify import markdownify as mdify
    except ImportError:
        return _clean_unit_text(html)
    try:
        soup = BeautifulSoup(html, "html.parser")
        main = soup.find("main") or soup.body or soup
        for tag in main.find_all(["script", "style", "nav", "header", "footer", "form", "button"]):
            tag.decompose()
        md = mdify(str(main), heading_style="ATX", strip=["img"])
        cleaned = _clean_markdown(md)
        return cleaned or _clean_unit_text(html)
    except Exception:
        return _clean_unit_text(html)


def _demote_headings(md: str) -> str:
    """Baja un nivel cada encabezado (h1->h2...) para que anide bajo el titulo de la leccion."""
    def repl(match: re.Match) -> str:
        hashes = match.group(1)
        return ("#" + hashes if len(hashes) < 6 else hashes) + " "
    return re.sub(r"^(#{1,6})\s+", repl, md, flags=re.M)


def _fetch_module_content(mod: dict, ctx: ssl.SSLContext | None) -> tuple[str, str]:
    """Baja todas las unidades de un modulo. Devuelve (markdown_legible, texto_plano).

    markdown_legible -> se muestra al estudiante (content_md).
    texto_plano       -> se trocea y embebe para el RAG del tutor.
    """
    base = mod["url"].split("?")[0]
    if not base.endswith("/"):
        base += "/"
    md_parts: list[str] = []
    text_parts: list[str] = []
    for index, unit_uid in enumerate(mod.get("units", []), start=1):
        slug = unit_uid.split(".")[-1]
        try:
            html = _http_get(f"{base}{index}-{slug}", ctx)
        except Exception:
            continue
        md = _demote_headings(_html_to_markdown(html))
        text = _clean_unit_text(html)
        if len(md) > 80:
            md_parts.append(md)
        if len(text) > 80:
            text_parts.append(text)
    return "\n\n---\n\n".join(md_parts), "\n\n".join(text_parts)


def _chunk_text(text: str, size: int = 1800, overlap: int = 200) -> list[str]:
    text = text.strip()
    if len(text) <= size:
        return [text] if len(text) > 60 else []
    chunks: list[str] = []
    start = 0
    while start < len(text):
        piece = text[start : start + size].strip()
        if len(piece) > 60:
            chunks.append(piece)
        start += size - overlap
    return chunks


def enrich_course_with_content(
    course: dict, mods_by_slug: dict, ctx, do_rag: bool
) -> int:
    """Descarga el contenido COMPLETO de cada leccion (una sola vez) y:

    - lo guarda como Markdown legible en lesson["content_md"] (lo que lee el estudiante);
    - si do_rag, trocea el texto plano, genera embeddings y lo sube a pgvector (tutor).

    Devuelve el numero de chunks subidos al RAG (0 si do_rag es False).
    """
    embed_documents = None
    upsert_lesson_chunks = None
    if do_rag:
        sys.path.insert(0, str(REPO_ROOT / "server"))
        from app.services.embedding_service import embed_documents
        from app.services.rag_service import upsert_lesson_chunks

    certification_code = course["certification_code"]
    total_chunks = 0
    total_lessons = sum(len(section["lessons"]) for section in course["sections"])
    lesson_index = 0
    for section in course["sections"]:
        for lesson in section["lessons"]:
            lesson_index += 1
            mod = mods_by_slug.get(lesson["lesson_key"])
            if not mod:
                continue
            print(
                f"    [{certification_code}] contenido {lesson_index}/{total_lessons}: {lesson.get('title')}"
            )
            markdown, plain_text = _fetch_module_content(mod, ctx)
            if len(markdown) > 80:
                source_url = mod["url"].split("?")[0]
                # Markdown legible + nota de la fuente oficial al pie.
                lesson["content_md"] = f"{markdown}\n\n---\n\n_Fuente oficial: {source_url}_"
            if do_rag and plain_text:
                chunks = _chunk_text(plain_text)
                if chunks:
                    embeddings = embed_documents(chunks)
                    upsert_lesson_chunks(
                        certification_code,
                        lesson["lesson_key"],
                        lesson.get("title"),
                        chunks,
                        embeddings,
                        mod["url"].split("?")[0],
                    )
                    total_chunks += len(chunks)
    return total_chunks


def _optional_lab_for_section(section_key: str, section_title: str) -> dict:
    return {
        "lab_key": f"lab-{section_key}",
        "title": f"Laboratorio opcional: aplica {section_title}",
        "is_optional": True,
        "estimated_minutes": 30,
        "instructions_md": (
            f"Lleva a la practica lo aprendido en **{section_title}**. "
            "Implementa un escenario pequeno y documenta tu solucion. "
            "Este laboratorio es opcional pero refuerza la retencion."
        ),
        "rubric": [
            {"criterion": "Funcionalidad", "weight": 40, "description": "La solucion cumple el objetivo del laboratorio."},
            {"criterion": "Claridad", "weight": 30, "description": "La explicacion es comprensible y ordenada."},
            {"criterion": "Buenas practicas", "weight": 30, "description": "Aplica recomendaciones del modulo."},
        ],
    }


def build_course_from_ms_learn(cert_code: str, cfg: dict, lps_by_uid: dict, mods_by_uid: dict) -> dict:
    uids: list[str] = list(cfg.get("learning_paths", []))
    for prefix in cfg.get("keyword_uid_prefix", []):
        for uid in lps_by_uid:
            if uid.startswith(prefix) and uid not in uids:
                uids.append(uid)

    sections: list[dict] = []
    total_minutes = 0
    for order, lp_uid in enumerate(uids, start=1):
        lp = lps_by_uid.get(lp_uid)
        if not lp:
            print(f"  ! learning path no encontrado en el catalogo: {lp_uid}")
            continue
        section_key = slugify(lp_uid)
        lessons: list[dict] = []
        section_minutes = 0
        for lesson_order, mod_uid in enumerate(lp.get("modules", []), start=1):
            mod = mods_by_uid.get(mod_uid)
            if not mod:
                continue
            minutes = int(mod.get("duration_in_minutes") or 0)
            section_minutes += minutes
            summary = (mod.get("summary") or "").strip()
            url = mod.get("url", "")
            lessons.append(
                {
                    "lesson_key": slugify(mod_uid),
                    "title": mod.get("title", mod_uid),
                    "order": lesson_order,
                    "duration_minutes": minutes,
                    "content_md": f"{summary}\n\nFuente oficial: {url}",
                    "learning_objectives": [],
                    "sources": [{"title": mod.get("title", "Microsoft Learn"), "url": url, "source": "ms_learn"}],
                }
            )
        if not lessons:
            continue
        total_minutes += section_minutes
        sections.append(
            {
                "section_key": section_key,
                "title": lp.get("title", lp_uid),
                "summary": (lp.get("summary") or "").strip() or None,
                "order": order,
                "duration_minutes": section_minutes,
                "lessons": lessons,
                "labs": [_optional_lab_for_section(section_key, lp.get("title", lp_uid))],
            }
        )

    return {
        "certification_code": cert_code,
        "track": cfg["track"],
        "title": cfg["title"],
        "summary": cfg["summary"],
        "provider": cfg["provider"],
        "level": cfg["level"],
        "total_duration_minutes": total_minutes,
        "source": "ms_learn",
        "source_url": "https://learn.microsoft.com/training/",
        "sections": sections,
    }


_LEVEL_MAP = {"beginner": "basic", "intermediate": "intermediate", "advanced": "advanced"}


def _lp_track(lp: dict) -> str | None:
    products = lp.get("products") or []
    if any("github" in p for p in products):
        return "github"
    if any("azure" in p for p in products):
        return "azure"
    return None


def build_course_from_learning_path(lp: dict, mods_by_uid: dict) -> dict | None:
    """Convierte un learning path de MS Learn en un curso (modo catalogo).

    course = learning path; sus modulos son las lecciones de una unica seccion.
    """
    track = _lp_track(lp)
    if track is None:
        return None
    provider = "GitHub" if track == "github" else "Microsoft"
    level = _LEVEL_MAP.get((lp.get("levels") or ["beginner"])[0], "basic")

    lessons: list[dict] = []
    total_minutes = 0
    for lesson_order, mod_uid in enumerate(lp.get("modules", []), start=1):
        mod = mods_by_uid.get(mod_uid)
        if not mod:
            continue
        minutes = int(mod.get("duration_in_minutes") or 0)
        total_minutes += minutes
        summary = (mod.get("summary") or "").strip()
        url = mod.get("url", "")
        lessons.append(
            {
                "lesson_key": slugify(mod_uid),
                "title": mod.get("title", mod_uid),
                "order": lesson_order,
                "duration_minutes": minutes,
                "content_md": f"{summary}\n\nFuente oficial: {url}",
                "learning_objectives": [],
                "sources": [{"title": mod.get("title", "Microsoft Learn"), "url": url, "source": "ms_learn"}],
            }
        )
    if not lessons:
        return None

    section_key = slugify(lp["uid"])
    return {
        "certification_code": slugify(lp["uid"], max_len=50),
        "track": track,
        "title": lp.get("title", lp["uid"]),
        "summary": (lp.get("summary") or "").strip() or None,
        "provider": provider,
        "level": level,
        "total_duration_minutes": total_minutes,
        "source": "ms_learn",
        "source_url": lp.get("url", "https://learn.microsoft.com/training/"),
        "sections": [
            {
                "section_key": section_key,
                "title": lp.get("title", lp["uid"]),
                "summary": (lp.get("summary") or "").strip() or None,
                "order": 1,
                "duration_minutes": total_minutes,
                "lessons": lessons,
                "labs": [_optional_lab_for_section(section_key, lp.get("title", lp["uid"]))],
            }
        ],
    }


def build_course_from_template(cert_code: str, template: dict) -> dict:
    sections: list[dict] = []
    total_minutes = 0
    for order, raw_section in enumerate(template["sections"], start=1):
        section_key = slugify(f"{cert_code}-{raw_section['title']}")
        lessons: list[dict] = []
        section_minutes = 0
        for lesson_order, raw_lesson in enumerate(raw_section["lessons"], start=1):
            minutes = int(raw_lesson.get("minutes") or 0)
            section_minutes += minutes
            source = raw_lesson.get("source", {})
            lessons.append(
                {
                    "lesson_key": slugify(f"{section_key}-{raw_lesson['title']}"),
                    "title": raw_lesson["title"],
                    "order": lesson_order,
                    "duration_minutes": minutes,
                    "content_md": (
                        f"{raw_lesson['title']}.\n\nFuente de referencia: "
                        f"{source.get('url', '')}"
                    ),
                    "learning_objectives": raw_lesson.get("objectives", []),
                    "sources": [{"title": source.get("title", "Documentacion"), "url": source.get("url", ""), "source": "synthetic"}],
                }
            )
        total_minutes += section_minutes
        sections.append(
            {
                "section_key": section_key,
                "title": raw_section["title"],
                "summary": raw_section.get("summary"),
                "order": order,
                "duration_minutes": section_minutes,
                "lessons": lessons,
                "labs": [_optional_lab_for_section(section_key, raw_section["title"])],
            }
        )
    return {
        "certification_code": cert_code,
        "track": template["track"],
        "title": template["title"],
        "summary": template["summary"],
        "provider": template["provider"],
        "level": template["level"],
        "total_duration_minutes": total_minutes,
        "source": "synthetic",
        "source_url": None,
        "sections": sections,
    }


def write_outputs(course: dict, out_dir: Path) -> None:
    cert_code = course["certification_code"]
    cert_slug = slugify(cert_code)

    # JSON snapshot
    courses_dir = out_dir / "courses"
    courses_dir.mkdir(parents=True, exist_ok=True)
    (courses_dir / f"{cert_slug}.json").write_text(
        json.dumps(course, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Markdown por leccion para indexar en Search / Foundry IQ.
    # Truncamos componentes del path para no superar el limite de 260 chars de Windows.
    cert_dir = out_dir / "certifications" / cert_slug[:40]
    cert_dir.mkdir(parents=True, exist_ok=True)
    for section in course["sections"]:
        section_dir = cert_dir / f"{section['order']:02d}-{section['section_key'][:36]}"
        section_dir.mkdir(parents=True, exist_ok=True)
        for lesson in section["lessons"]:
            objectives = "\n".join(f"- {item}" for item in lesson.get("learning_objectives", []))
            sources = "\n".join(
                f"- [{s.get('title','fuente')}]({s.get('url','')})" for s in lesson.get("sources", [])
            )
            body = (
                f"# {lesson['title']}\n\n"
                f"> Curso: {course['title']} ({cert_code}) · Seccion: {section['title']}\n"
                f"> Duracion estimada: {lesson.get('duration_minutes', 0)} min\n\n"
                f"## Objetivos\n{objectives or '- (pendiente de expansion por agente)'}\n\n"
                f"## Contenido\n{lesson.get('content_md','')}\n\n"
                f"## Fuentes\n{sources or '- (sin fuente)'}\n"
            )
            (section_dir / f"{lesson['order']:02d}-{lesson['lesson_key'][:36]}.md").write_text(
                body, encoding="utf-8"
            )


def push_to_supabase(course: dict) -> None:
    sys.path.insert(0, str(REPO_ROOT / "server"))
    from app.models.course import CourseDetail
    from app.services.course_service import upsert_course

    course_id = upsert_course(CourseDetail.model_validate(course))
    print(f"  -> Supabase upsert ok (course_id={course_id})")


def _run_catalog_mode(args, ctx, out_dir: Path) -> int:
    products = {p.strip() for p in args.products.split(",") if p.strip()}
    levels = {l.strip() for l in args.levels.split(",") if l.strip()}
    print("Descargando catalogo de Microsoft Learn (modo catalogo)...")
    lps_by_uid, mods_by_uid = fetch_catalog(ctx)
    print(f"  learningPaths={len(lps_by_uid)} modules={len(mods_by_uid)}")

    def matches(lp: dict) -> bool:
        lp_products = lp.get("products") or []
        if products and not any(any(p in x for x in lp_products) for p in products):
            return False
        if levels and not (set(lp.get("levels") or []) & levels):
            return False
        return True

    candidates = [lp for lp in lps_by_uid.values() if matches(lp)]
    print(f"  candidatos tras filtro (products={products}, levels={levels or 'todos'}): {len(candidates)}")

    want_content = args.content or args.rag
    mods_by_slug = {slugify(uid): mod for uid, mod in mods_by_uid.items()} if want_content else {}
    if want_content:
        print(f"  contenido completo: ON (rag={'si' if args.rag else 'no'}) — la descarga tomara mas tiempo")

    built = 0
    skipped = 0
    exit_code = 0
    for lp in candidates:
        if args.limit and built >= args.limit:
            break
        try:
            course = build_course_from_learning_path(lp, mods_by_uid)
            if not course:
                skipped += 1
                continue
            if want_content:
                chunk_count = enrich_course_with_content(course, mods_by_slug, ctx, do_rag=args.rag)
                if args.rag:
                    print(f"  {course['certification_code']}: contenido + {chunk_count} chunks RAG")
            write_outputs(course, out_dir)
            if args.push:
                push_to_supabase(course)
            built += 1
            if built % 25 == 0:
                print(f"  ... {built} cursos generados")
        except Exception as exc:  # pragma: no cover
            print(f"  ! error en {lp.get('uid')}: {type(exc).__name__}: {exc}")
            exit_code = 1

    # Ademas, AWS sintetico para no dejar fuera ese track.
    try:
        aws = build_course_from_template("AWS Cloud Practitioner", SYNTHETIC_CERTS["AWS Cloud Practitioner"])
        write_outputs(aws, out_dir)
        if args.push:
            push_to_supabase(aws)
        built += 1
    except Exception as exc:  # pragma: no cover
        print(f"  ! error en AWS sintetico: {exc}")

    print(f"\nModo catalogo terminado: {built} cursos generados, {skipped} omitidos (sin modulos).")
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingesta de cursos para RetAIM.")
    parser.add_argument("--certs", nargs="*", help="Codigos de certificacion a procesar. Default: todos.")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Carpeta de salida (default: synthetic-data).")
    parser.add_argument("--push", action="store_true", help="Subir los cursos a Supabase via course_service.")
    parser.add_argument("--insecure-ssl", action="store_true",
                        help="Desactiva verificacion TLS (solo si tu red rompe la cadena de certificados).")
    parser.add_argument("--catalog", action="store_true",
                        help="Modo catalogo: ingesta TODOS los learning paths de MS Learn como cursos (cientos).")
    parser.add_argument("--products", default="azure,github",
                        help="Productos a incluir en modo catalogo (default: azure,github).")
    parser.add_argument("--levels", default="beginner,intermediate",
                        help="Niveles a incluir en modo catalogo (default: beginner,intermediate). Vacio = todos.")
    parser.add_argument("--limit", type=int, default=50,
                        help="Maximo de cursos en modo catalogo (default 50; 0 = sin limite).")
    parser.add_argument("--content", action="store_true",
                        help="Baja el contenido COMPLETO de cada leccion desde MS Learn y lo guarda "
                             "como Markdown legible en content_md (lo que lee el estudiante). Mas lento.")
    parser.add_argument("--rag", action="store_true",
                        help="Ademas de --content, trocea el texto, genera embeddings (multilingual-e5-large) y los "
                             "guarda en Supabase pgvector para el tutor. Implica --content. Requiere --push.")
    args = parser.parse_args()

    if args.rag and not args.push:
        parser.error("--rag requiere --push (los embeddings se guardan en Supabase).")

    insecure = args.insecure_ssl or os.environ.get("INGEST_INSECURE_SSL") == "1"
    ctx = make_ssl_context(insecure)
    out_dir = Path(args.out)

    if args.catalog:
        return _run_catalog_mode(args, ctx, out_dir)

    all_certs = list(MS_LEARN_CERTS.keys()) + list(SYNTHETIC_CERTS.keys())
    targets = args.certs or all_certs

    lps_by_uid: dict = {}
    mods_by_uid: dict = {}
    if any(cert in MS_LEARN_CERTS for cert in targets):
        print("Descargando catalogo de Microsoft Learn...")
        lps_by_uid, mods_by_uid = fetch_catalog(ctx)
        print(f"  learningPaths={len(lps_by_uid)} modules={len(mods_by_uid)}")

    want_content = args.content or args.rag
    mods_by_slug = {slugify(uid): mod for uid, mod in mods_by_uid.items()} if want_content else {}

    exit_code = 0
    for cert_code in targets:
        print(f"\n== {cert_code} ==")
        try:
            if cert_code in MS_LEARN_CERTS:
                course = build_course_from_ms_learn(cert_code, MS_LEARN_CERTS[cert_code], lps_by_uid, mods_by_uid)
            elif cert_code in SYNTHETIC_CERTS:
                course = build_course_from_template(cert_code, SYNTHETIC_CERTS[cert_code])
            else:
                print(f"  ! cert no reconocido: {cert_code}")
                exit_code = 1
                continue

            section_count = len(course["sections"])
            lesson_count = sum(len(s["lessons"]) for s in course["sections"])
            print(f"  secciones={section_count} lecciones={lesson_count} min_total={course['total_duration_minutes']}")
            if section_count == 0:
                print("  ! curso sin secciones, se omite.")
                exit_code = 1
                continue

            if want_content and course.get("source") == "ms_learn":
                chunk_count = enrich_course_with_content(course, mods_by_slug, ctx, do_rag=args.rag)
                print(f"  contenido completo cargado{f' + {chunk_count} chunks RAG' if args.rag else ''}")

            write_outputs(course, out_dir)
            print(f"  archivos escritos en {out_dir}")
            if args.push:
                push_to_supabase(course)
        except Exception as exc:  # pragma: no cover
            print(f"  ! error procesando {cert_code}: {type(exc).__name__}: {exc}")
            exit_code = 1

    print("\nIngesta terminada.")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
