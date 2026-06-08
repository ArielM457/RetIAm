"""RAG sobre Supabase pgvector.

- `upsert_lesson_chunks`: guarda los fragmentos + embeddings de una leccion
  (lo usa la ingesta).
- `retrieve`: embebe la pregunta y recupera los fragmentos mas similares del curso
  via la funcion SQL `match_lesson_chunks`.

Todo degrada con gracia: si fastembed/pgvector fallan, devuelve lista vacia y el
tutor cae a su fallback.
"""

import logging

from app.core.config import get_settings
from app.db.supabase import get_supabase_service_client
from app.services._shared import response_data
from app.services.embedding_service import embed_query

logger = logging.getLogger(__name__)


def upsert_lesson_chunks(
    certification_code: str,
    lesson_key: str,
    lesson_title: str | None,
    chunks: list[str],
    embeddings: list[list[float]],
    source_url: str | None,
) -> int:
    settings = get_settings()
    client = get_supabase_service_client()
    # Idempotente: borra los chunks previos de esa leccion antes de reinsertar.
    client.table(settings.supabase_lesson_chunks_table).delete().eq(
        "certification_code", certification_code
    ).eq("lesson_key", lesson_key).execute()

    rows = [
        {
            "certification_code": certification_code,
            "lesson_key": lesson_key,
            "lesson_title": lesson_title,
            "content": chunk,
            "source_url": source_url,
            "chunk_index": index,
            "embedding": embedding,
        }
        for index, (chunk, embedding) in enumerate(zip(chunks, embeddings, strict=False))
    ]
    if rows:
        client.table(settings.supabase_lesson_chunks_table).insert(rows).execute()
    return len(rows)


def retrieve(certification_code: str | None, query: str, k: int = 5) -> list[dict]:
    """Devuelve los fragmentos mas relevantes del curso para la pregunta."""
    try:
        query_embedding = embed_query(query)
    except Exception as exc:
        logger.warning("No se pudo generar el embedding de la consulta: %s", exc)
        return []
    try:
        response = (
            get_supabase_service_client()
            .rpc(
                "match_lesson_chunks",
                {
                    "query_embedding": query_embedding,
                    "match_count": k,
                    "filter_certification": certification_code,
                },
            )
            .execute()
        )
        return response_data(response, []) or []
    except Exception as exc:
        logger.warning("Falla en match_lesson_chunks (RAG): %s", exc)
        return []
