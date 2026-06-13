"""Síntesis de voz (TTS) con Azure AI Speech para la Sala de Auxiliaturas.

Usa la API REST de Azure Speech (no requiere SDK). Si no hay key/region
configuradas, `speech_enabled()` devuelve False y el frontend cae a la voz del
navegador.
"""

from __future__ import annotations

import html
import logging

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)

# mp3 ligero, suficiente para narración en la web.
_OUTPUT_FORMAT = "audio-24khz-48kbitrate-mono-mp3"


def speech_enabled() -> bool:
    """True si hay credenciales de Azure Speech configuradas."""
    settings = get_settings()
    return bool(settings.azure_speech_key and settings.azure_speech_region)


def _lang_from_voice(voice: str) -> str:
    """De 'es-ES-ElviraNeural' saca 'es-ES'."""
    parts = voice.split("-")
    return "-".join(parts[:2]) if len(parts) >= 2 else "es-ES"


def synthesize(text: str, voice: str | None = None) -> bytes | None:
    """Devuelve audio mp3 (bytes) para `text`, o None si falla / no está activo."""
    settings = get_settings()
    if not speech_enabled():
        return None

    voice = voice or settings.azure_speech_voice
    lang = _lang_from_voice(voice)
    ssml = (
        f"<speak version='1.0' xml:lang='{lang}'>"
        f"<voice xml:lang='{lang}' name='{voice}'>{html.escape(text)}</voice>"
        f"</speak>"
    )
    url = (
        f"https://{settings.azure_speech_region}.tts.speech.microsoft.com"
        "/cognitiveservices/v1"
    )
    headers = {
        "Ocp-Apim-Subscription-Key": settings.azure_speech_key or "",
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": _OUTPUT_FORMAT,
        "User-Agent": "retaim-auxiliaturas",
    }
    try:
        resp = httpx.post(url, headers=headers, content=ssml.encode("utf-8"), timeout=30.0)
        resp.raise_for_status()
        return resp.content
    except Exception as exc:  # noqa: BLE001
        logger.warning("Azure Speech TTS falló: %s", exc)
        return None
