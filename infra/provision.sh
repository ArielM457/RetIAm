#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=infra/lib.sh
source "${SCRIPT_DIR}/lib.sh"

require_command az
require_command curl
PYTHON_CMD="$(detect_python_cmd)"

load_optional_env_file "${1:-}"

RESOURCE_GROUP="${RESOURCE_GROUP:-retaim-hackathon-rg}"
LOCATION="${LOCATION:-eastus}"
PROJECT_PREFIX="${PROJECT_PREFIX:-retaim}"
SKIP_AGENTS="${SKIP_AGENTS:-false}"

log "Validando sesion de Azure"
az account show >/dev/null
AZURE_SUBSCRIPTION_ID="$(az_tsv account show --query id)"
set_output_var AZURE_SUBSCRIPTION_ID "${AZURE_SUBSCRIPTION_ID}"

register_resource_providers

log "Creando resource group ${RESOURCE_GROUP} en ${LOCATION}"
az group create --name "${RESOURCE_GROUP}" --location "${LOCATION}" >/dev/null
set_output_var RESOURCE_GROUP "${RESOURCE_GROUP}"
set_output_var LOCATION "${LOCATION}"

"${SCRIPT_DIR}/foundry.sh"
"${SCRIPT_DIR}/knowledge_base.sh"
"${SCRIPT_DIR}/static_web.sh"
"${SCRIPT_DIR}/container_apps.sh"

if [[ "${SKIP_AGENTS}" != "true" ]]; then
  log "Creando agentes Gini"
  AGENTS_JSON="${OUTPUT_DIR}/agents.json"
  "${PYTHON_CMD}" "${SCRIPT_DIR}/agents/create_agents.py" \
    --config-dir "${SCRIPT_DIR}/agents/agent_configs" \
    --output "${AGENTS_JSON}"

  while IFS='=' read -r key value; do
    set_output_var "${key}" "${value}"
  done < <(
    "${PYTHON_CMD}" - "${AGENTS_JSON}" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    data = json.load(handle)

for key, value in sorted(data.items()):
    print(f"{key}={value}")
PY
  )
else
  warn "SKIP_AGENTS=true. Se omite la creacion de agentes."
fi

render_env_file

log "Provisioning terminado"
printf '\nArchivo de salida: %s\n' "${OUTPUT_ENV_FILE}"
printf 'Foundry endpoint: %s\n' "${AZURE_FOUNDRY_ENDPOINT:-}"
printf 'Search endpoint: %s\n' "${AZURE_SEARCH_ENDPOINT:-}"
printf 'Blob account: %s\n' "${AZURE_STORAGE_ACCOUNT:-}"
printf 'Backend URL: %s\n' "${BACKEND_CONTAINER_APP_URL:-pendiente}"
printf 'Frontend URL: %s\n' "${STATIC_WEB_APP_URL:-pendiente}"
printf '\nVariables Supabase que aun debes completar manualmente:\n'
printf 'SUPABASE_URL\nSUPABASE_ANON_KEY\nSUPABASE_SERVICE_ROLE_KEY\n'
