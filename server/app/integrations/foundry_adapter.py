"""Adaptador de Azure AI Foundry (Fase 2).

Expone `run_agent(...)` que ejecuta uno de los agentes Gini contra el modelo
desplegado en Foundry, con grounding opcional en Azure AI Search (Foundry IQ).

La "personalidad" de cada agente se carga desde sus configs en
`infra/agents/agent_configs/gini-*.json`, de modo que el mismo system prompt que
crea los agentes en Foundry se usa aqui (una sola fuente de verdad).

Todo es best-effort: si Foundry no esta configurado, el SDK no esta instalado, o
la llamada falla, `run_agent` devuelve None y el llamador cae a su comportamiento
mock. Asi el backend funciona siempre, con o sin Azure.
"""

import json
import logging
from functools import lru_cache
from pathlib import Path

from app.core.config import get_settings

logger = logging.getLogger(__name__)

_AGENT_CONFIG_DIR = Path(__file__).resolve().parents[3] / "infra" / "agents" / "agent_configs"

_DEFAULT_INSTRUCTIONS = {
    "gini-path": "Eres Gini Path. Construyes y adaptas contenido de aprendizaje fundamentado para certificaciones tecnicas. Nunca inventes datos fuera de las fuentes.",
    "gini-eval": "Eres Gini Eval. Generas preguntas y respondes dudas fundamentadas en el contenido estudiado, citando la fuente.",
    "gini-insight": "Eres Gini Insight. Analizas preferencias y comportamiento para mejorar la experiencia de aprendizaje.",
}


def foundry_enabled() -> bool:
    settings = get_settings()
    return bool(
        settings.enable_external_ai
        and settings.azure_foundry_endpoint
        and settings.azure_foundry_deployment
        and settings.azure_foundry_api_key
    )


def search_grounding_enabled() -> bool:
    settings = get_settings()
    return bool(
        settings.azure_search_endpoint and settings.azure_search_key and settings.azure_search_index
    )


@lru_cache(maxsize=16)
def _agent_instructions(agent_name: str) -> str:
    config_path = _AGENT_CONFIG_DIR / f"{agent_name}.json"
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
        instructions = data.get("instructions")
        if instructions:
            return instructions
    except Exception as exc:  # pragma: no cover - depende del FS
        logger.debug("No se pudo leer config de %s: %s", agent_name, exc)
    return _DEFAULT_INSTRUCTIONS.get(agent_name, "Eres un agente de RetAIM.")


def _search_data_sources() -> list | None:
    if not search_grounding_enabled():
        return None
    settings = get_settings()
    return [
        {
            "type": "azure_search",
            "parameters": {
                "endpoint": settings.azure_search_endpoint,
                "index_name": settings.azure_search_index,
                "authentication": {"type": "api_key", "key": settings.azure_search_key},
            },
        }
    ]


def _extract_citations(message) -> list[dict]:
    context = getattr(message, "context", None)
    if context is None and hasattr(message, "model_extra"):
        context = (message.model_extra or {}).get("context")
    if not isinstance(context, dict):
        return []
    citations = context.get("citations") or []
    sources: list[dict] = []
    for citation in citations:
        if not isinstance(citation, dict):
            continue
        sources.append(
            {
                "title": citation.get("title") or citation.get("filepath") or "Fuente",
                "url": citation.get("url") or citation.get("filepath"),
                "source": "foundry_iq",
            }
        )
    return sources


def run_agent(
    agent_name: str,
    user_prompt: str,
    *,
    temperature: float = 0.4,
    max_tokens: int = 900,
    ground: bool = True,
    response_json: bool = False,
    deployment: str | None = None,
) -> dict | None:
    """Ejecuta un agente Gini en Foundry. Devuelve dict o None (fallback).

    dict: {"text": str, "sources": list[dict], "source_mode": "foundry"}

    `deployment` permite usar otro modelo desplegado (p. ej. gpt-4.1-mini para la
    Sala 1) sin cambiar el resto; si es None usa azure_foundry_deployment.
    """
    if not foundry_enabled():
        return None
    try:
        from openai import AzureOpenAI
    except ImportError:
        logger.warning("openai SDK no instalado; Foundry deshabilitado en runtime. Instala server/requirements.txt.")
        return None

    settings = get_settings()
    try:
        client = AzureOpenAI(
            azure_endpoint=settings.azure_foundry_endpoint,
            api_key=settings.azure_foundry_api_key,
            api_version=settings.azure_foundry_api_version,
        )
        messages = [
            {"role": "system", "content": _agent_instructions(agent_name)},
            {"role": "user", "content": user_prompt},
        ]
        kwargs: dict = {
            "model": deployment or settings.azure_foundry_deployment,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if response_json:
            kwargs["response_format"] = {"type": "json_object"}
        extra_body = {}
        if ground:
            data_sources = _search_data_sources()
            if data_sources:
                extra_body["data_sources"] = data_sources
        if extra_body:
            kwargs["extra_body"] = extra_body

        response = client.chat.completions.create(**kwargs)
        choice = response.choices[0]
        text = (choice.message.content or "").strip()
        if not text:
            return None
        return {
            "text": text,
            "sources": _extract_citations(choice.message),
            "source_mode": "foundry",
        }
    except Exception as exc:
        logger.warning("Fallo la llamada a Foundry (%s); se usa fallback mock: %s", agent_name, exc)
        return None


def run_agent_json(agent_name: str, user_prompt: str, **kwargs) -> dict | None:
    """Como run_agent pero parsea la respuesta como JSON. Devuelve el objeto o None."""
    result = run_agent(agent_name, user_prompt, response_json=True, **kwargs)
    if not result:
        return None
    try:
        parsed = json.loads(result["text"])
    except (json.JSONDecodeError, KeyError):
        logger.warning("Respuesta de %s no era JSON valido.", agent_name)
        return None
    parsed["_sources"] = result.get("sources", [])
    return parsed
