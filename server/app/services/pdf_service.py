"""Generacion de PDFs sin dependencias externas (Fase 5).

`generate_certificate_pdf` arma un certificado RetAIM con diseño (apaisado, borde,
branding, codigo de verificacion). `generate_simple_pdf` se conserva para usos
genericos (resumenes, etc.).
"""

from pathlib import Path

# Ancho aproximado de caracter para Helvetica (fraccion del font size).
_CHAR_W = 0.52


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _text_width(text: str, size: float) -> float:
    return len(text) * size * _CHAR_W


def _centered(text: str, size: float, y: int, page_width: int, font: str = "F1") -> str:
    x = max(20, (page_width - _text_width(text, size)) / 2)
    return f"BT /{font} {size:.0f} Tf 1 0 0 1 {x:.1f} {y} Tm ({_escape(text)}) Tj ET"


def _build_pdf(content_stream: str, page_width: int, page_height: int) -> bytes:
    stream = content_stream.encode("latin-1", errors="replace")
    objects: list[bytes] = []
    objects.append(b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n")
    objects.append(b"2 0 obj << /Type /Pages /Count 1 /Kids [3 0 R] >> endobj\n")
    objects.append(
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 "
        + f"{page_width} {page_height}".encode("latin-1")
        + b"] /Resources << /Font << /F1 4 0 R /F2 6 0 R >> >> /Contents 5 0 R >> endobj\n"
    )
    objects.append(b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n")
    objects.append(
        f"5 0 obj << /Length {len(stream)} >> stream\n".encode("latin-1")
        + stream
        + b"\nendstream endobj\n"
    )
    objects.append(b"6 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >> endobj\n")

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for item in objects:
        offsets.append(len(pdf))
        pdf.extend(item)
    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(offsets)}\n".encode("latin-1"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))
    pdf.extend(
        f"trailer << /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF".encode("latin-1")
    )
    return bytes(pdf)


def generate_certificate_pdf(
    output_path: Path,
    *,
    recipient: str,
    certification: str,
    score: int,
    date_str: str,
    verification_code: str,
    verify_url: str | None = None,
    summary: str | None = None,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    w, h = 792, 612  # apaisado (letter landscape)

    # Borde doble (rectangulos) con color violeta.
    ops: list[str] = []
    ops.append("0.31 0.27 0.90 RG 3 w")  # indigo
    ops.append(f"30 30 {w - 60} {h - 60} re S")
    ops.append("0.49 0.23 0.93 RG 1 w")  # violeta
    ops.append(f"42 42 {w - 84} {h - 84} re S")

    # Texto centrado (negro/violeta segun jerarquia).
    ops.append("0 0 0 rg")
    ops.append(_centered("RetAIM", 22, h - 110, w, font="F2"))
    ops.append("0.49 0.23 0.93 rg")
    ops.append(_centered("CERTIFICADO DE LOGRO", 30, h - 160, w, font="F2"))
    ops.append("0 0 0 rg")
    ops.append(_centered("Se otorga este certificado a", 14, h - 215, w))
    ops.append("0.31 0.27 0.90 rg")
    ops.append(_centered(recipient, 38, h - 270, w, font="F2"))
    ops.append("0 0 0 rg")
    ops.append(_centered("por completar exitosamente la certificacion", 14, h - 315, w))
    ops.append(_centered(certification, 22, h - 350, w, font="F2"))
    ops.append(_centered(f"Puntaje final: {score} / 100", 16, h - 390, w))
    if summary:
        ops.append(_centered(summary[:90], 11, h - 420, w))
    ops.append(_centered(f"Fecha de emision: {date_str}", 12, h - 455, w))

    # Footer de verificacion.
    ops.append("0.40 0.40 0.40 rg")
    ops.append(_centered(f"Codigo de verificacion: {verification_code}", 11, 90, w))
    if verify_url:
        ops.append(_centered(f"Verifica en: {verify_url}", 10, 72, w))
    ops.append(_centered("Datos sinteticos para demostracion - RetAIM", 9, 56, w))

    output_path.write_bytes(_build_pdf("\n".join(ops), w, h))


def generate_simple_pdf(output_path: Path, title: str, lines: list[str]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    w, h = 612, 792
    ops: list[str] = [f"BT /F2 18 Tf 1 0 0 1 50 {h - 60} Tm ({_escape(title)}) Tj ET"]
    y = h - 95
    for line in lines:
        ops.append(f"BT /F1 11 Tf 1 0 0 1 50 {y} Tm ({_escape(line)}) Tj ET")
        y -= 20
    output_path.write_bytes(_build_pdf("\n".join(ops), w, h))
