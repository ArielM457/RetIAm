"""Voz de la Sala de Auxiliaturas: estado + síntesis de voz (TTS) con Azure Speech."""

from fastapi import APIRouter, Depends, HTTPException, Response

from app.core.config import get_settings
from app.core.security import get_current_supabase_user
from app.models.speech import SpeechStatus, TtsRequest
from app.services.speech_service import speech_enabled, synthesize

router = APIRouter()


@router.get("/status", response_model=SpeechStatus)
def get_status() -> SpeechStatus:
    """Indica al frontend si usar voz neuronal de Azure o caer al navegador."""
    return SpeechStatus(enabled=speech_enabled(), voice=get_settings().azure_speech_voice)


@router.post("/tts")
def post_tts(
    payload: TtsRequest,
    current_user=Depends(get_current_supabase_user),
) -> Response:
    text = (payload.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="El texto a narrar está vacío.")
    audio = synthesize(text[:3000], payload.voice)
    if audio is None:
        raise HTTPException(status_code=503, detail="Azure Speech no está disponible.")
    return Response(content=audio, media_type="audio/mpeg")
