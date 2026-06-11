"""Generacion de embeddings para el RAG (Supabase pgvector).

Usa fastembed (ONNX, corre en CPU, sin GPU ni torch) con un modelo multilingue
gratuito. Por defecto multilingual-e5-large (1024 dim), fuerte en espanol/ingles
(requiere prefijos query:/passage:, que aplicamos abajo).

El modelo se carga una sola vez (lru_cache). Si fastembed no esta instalado o el
modelo falla, las funciones lanzan/avisan y el llamador cae a su fallback.
"""

import logging
from functools import lru_cache
from pathlib import Path
import shutil

from app.core.config import get_settings

logger = logging.getLogger(__name__)

_EMBED_CACHE_DIR = Path(__file__).resolve().parents[2] / "generated" / "fastembed_cache"


def embedding_available() -> bool:
    try:
        import fastembed  # noqa: F401

        return True
    except ImportError:
        return False


@lru_cache(maxsize=1)
def _model():
    from fastembed import TextEmbedding

    settings = get_settings()
    logger.info("Cargando modelo de embeddings: %s", settings.embedding_model)
    _EMBED_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    try:
        return TextEmbedding(
            model_name=settings.embedding_model,
            cache_dir=str(_EMBED_CACHE_DIR),
        )
    except Exception as exc:
        message = str(exc)
        if "model.onnx_data" not in message and "External data path" not in message:
            raise

        logger.warning(
            "Cache de fastembed corrupto o incompleto en %s. Se limpiara y se reintentara una vez.",
            _EMBED_CACHE_DIR,
        )
        shutil.rmtree(_EMBED_CACHE_DIR, ignore_errors=True)
        _EMBED_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        return TextEmbedding(
            model_name=settings.embedding_model,
            cache_dir=str(_EMBED_CACHE_DIR),
        )


def _is_e5() -> bool:
    # Los modelos e5 requieren prefijos "query:"/"passage:"; bge-m3 no.
    return "e5" in get_settings().embedding_model.lower()


def embed_documents(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    prefix = "passage: " if _is_e5() else ""
    vectors = _model().embed([prefix + text for text in texts])
    return [[float(value) for value in vector] for vector in vectors]


def embed_query(text: str) -> list[float]:
    prefix = "query: " if _is_e5() else ""
    vector = next(iter(_model().embed([prefix + text])))
    return [float(value) for value in vector]
