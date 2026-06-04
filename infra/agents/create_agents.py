from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def load_sdk():
    try:
        from azure.ai.projects import AIProjectClient
        from azure.ai.projects.models import PromptAgentDefinition
        from azure.identity import DefaultAzureCredential
    except ImportError as exc:  # pragma: no cover - depends on local env
        raise SystemExit(
            "Faltan dependencias para crear agentes. "
            "Instala infra/agents/requirements.txt antes de ejecutar este script."
        ) from exc

    return AIProjectClient, PromptAgentDefinition, DefaultAzureCredential


def read_config(config_path: Path) -> dict:
    return json.loads(config_path.read_text(encoding="utf-8"))


def iter_configs(config_dir: Path) -> list[Path]:
    return sorted(config_dir.glob("*.json"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Crea los agentes Gini en Azure AI Foundry.")
    parser.add_argument("--config-dir", required=True, help="Carpeta con archivos JSON de agentes.")
    parser.add_argument("--output", required=True, help="Archivo de salida con ids creados.")
    args = parser.parse_args()

    config_dir = Path(args.config_dir)
    output_path = Path(args.output)

    if not config_dir.exists():
        raise SystemExit(f"No existe la carpeta de configuracion: {config_dir}")

    config_files = iter_configs(config_dir)
    if not config_files:
        raise SystemExit(f"No se encontraron archivos JSON en {config_dir}")

    endpoint = os.environ.get("AZURE_FOUNDRY_ENDPOINT")
    model_deployment = os.environ.get("AZURE_FOUNDRY_DEPLOYMENT", "gpt-4o-mini")
    if not endpoint:
        raise SystemExit("Falta AZURE_FOUNDRY_ENDPOINT en el entorno.")

    AIProjectClient, PromptAgentDefinition, DefaultAzureCredential = load_sdk()
    client = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())

    created_agents: dict[str, str] = {}

    for config_path in config_files:
        config = read_config(config_path)
        agent_name = config["name"]
        definition = PromptAgentDefinition(
            name=agent_name,
            model=config.get("model", model_deployment),
            description=config.get("description", ""),
            instructions=config["instructions"],
        )
        agent = client.agents.create_version(definition)
        env_key = config.get("output_env", agent_name.upper().replace("-", "_"))
        created_agents[env_key] = getattr(agent, "id", "")
        print(f"Agente creado: {agent_name} -> {created_agents[env_key]}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(created_agents, indent=2, sort_keys=True), encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
