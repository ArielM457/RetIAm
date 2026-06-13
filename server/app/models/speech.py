"""Modelos para el endpoint de voz (TTS) de la Sala de Auxiliaturas."""

from pydantic import BaseModel


class TtsRequest(BaseModel):
    text: str
    voice: str | None = None


class SpeechStatus(BaseModel):
    enabled: bool
    voice: str
