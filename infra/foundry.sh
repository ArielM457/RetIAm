#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=infra/lib.sh
source "${SCRIPT_DIR}/lib.sh"

require_command az
PYTHON_CMD="$(detect_python_cmd)"

: "${RESOURCE_GROUP:?Debes definir RESOURCE_GROUP}"
: "${LOCATION:?Debes definir LOCATION}"

PROJECT_PREFIX="${PROJECT_PREFIX:-retaim}"
SUFFIX="${SUFFIX:-$(date '+%m%d%H%M')}"
BASE_NAME="$(sanitize_name "${PROJECT_PREFIX}${SUFFIX}")"

AZURE_FOUNDRY_RESOURCE_NAME="${AZURE_FOUNDRY_RESOURCE_NAME:-${BASE_NAME}foundry}"
AZURE_FOUNDRY_PROJECT="${AZURE_FOUNDRY_PROJECT:-${PROJECT_PREFIX}-project}"
AZURE_FOUNDRY_DEPLOYMENT="${AZURE_FOUNDRY_DEPLOYMENT:-gpt-4o-mini}"

log "Creando recurso de Foundry ${AZURE_FOUNDRY_RESOURCE_NAME}"
if ! az cognitiveservices account show --name "${AZURE_FOUNDRY_RESOURCE_NAME}" --resource-group "${RESOURCE_GROUP}" >/dev/null 2>&1; then
  az cognitiveservices account create \
    --name "${AZURE_FOUNDRY_RESOURCE_NAME}" \
    --resource-group "${RESOURCE_GROUP}" \
    --kind AIServices \
    --sku S0 \
    --location "${LOCATION}" \
    --allow-project-management \
    --yes >/dev/null

  az cognitiveservices account update \
    --name "${AZURE_FOUNDRY_RESOURCE_NAME}" \
    --resource-group "${RESOURCE_GROUP}" \
    --custom-domain "${AZURE_FOUNDRY_RESOURCE_NAME}" >/dev/null
fi

log "Creando proyecto de Foundry ${AZURE_FOUNDRY_PROJECT}"
if ! az cognitiveservices account project show \
  --name "${AZURE_FOUNDRY_RESOURCE_NAME}" \
  --resource-group "${RESOURCE_GROUP}" \
  --project-name "${AZURE_FOUNDRY_PROJECT}" >/dev/null 2>&1; then
  az cognitiveservices account project create \
    --name "${AZURE_FOUNDRY_RESOURCE_NAME}" \
    --resource-group "${RESOURCE_GROUP}" \
    --project-name "${AZURE_FOUNDRY_PROJECT}" \
    --location "${LOCATION}" >/dev/null
fi

PROJECT_JSON="$(az_json cognitiveservices account project show \
  --name "${AZURE_FOUNDRY_RESOURCE_NAME}" \
  --resource-group "${RESOURCE_GROUP}" \
  --project-name "${AZURE_FOUNDRY_PROJECT}")"

FOUNDRY_ENDPOINT="$("${PYTHON_CMD}" -c 'import json,sys; data=json.load(sys.stdin); print(data.get("properties",{}).get("endpoint",""))' <<<"${PROJECT_JSON}")"
FOUNDRY_KEY="$(az_tsv cognitiveservices account keys list \
  --name "${AZURE_FOUNDRY_RESOURCE_NAME}" \
  --resource-group "${RESOURCE_GROUP}" \
  --query key1)"

set_output_var AZURE_FOUNDRY_RESOURCE_NAME "${AZURE_FOUNDRY_RESOURCE_NAME}"
set_output_var AZURE_FOUNDRY_PROJECT "${AZURE_FOUNDRY_PROJECT}"
set_output_var AZURE_FOUNDRY_ENDPOINT "${FOUNDRY_ENDPOINT}"
set_output_var AZURE_FOUNDRY_API_KEY "${FOUNDRY_KEY}"
set_output_var AZURE_FOUNDRY_DEPLOYMENT "${AZURE_FOUNDRY_DEPLOYMENT}"

log "Foundry listo"
