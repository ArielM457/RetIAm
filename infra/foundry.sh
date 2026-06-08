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
AZURE_FOUNDRY_DEPLOYMENT="${AZURE_FOUNDRY_DEPLOYMENT:-gpt-4o}"

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

# gpt-4o 2024-11-20 (vigente). La version 2024-07-18 de gpt-4o-mini quedo deprecada (03/2026).
AZURE_FOUNDRY_MODEL_NAME="${AZURE_FOUNDRY_MODEL_NAME:-gpt-4o}"
AZURE_FOUNDRY_MODEL_VERSION="${AZURE_FOUNDRY_MODEL_VERSION:-2024-11-20}"
AZURE_FOUNDRY_MODEL_CAPACITY="${AZURE_FOUNDRY_MODEL_CAPACITY:-10}"
# SKUs a intentar, en orden. Las cuentas Azure for Students suelen tener cuota en
# 'Standard' (no en 'GlobalStandard'). Puedes forzar uno con AZURE_FOUNDRY_MODEL_SKU.
AZURE_FOUNDRY_MODEL_SKUS="${AZURE_FOUNDRY_MODEL_SKU:-Standard GlobalStandard DataZoneStandard}"

log "Desplegando modelo ${AZURE_FOUNDRY_MODEL_NAME} (deployment ${AZURE_FOUNDRY_DEPLOYMENT})"
if ! az cognitiveservices account deployment show \
  --name "${AZURE_FOUNDRY_RESOURCE_NAME}" \
  --resource-group "${RESOURCE_GROUP}" \
  --deployment-name "${AZURE_FOUNDRY_DEPLOYMENT}" >/dev/null 2>&1; then
  deployed_sku=""
  for sku in ${AZURE_FOUNDRY_MODEL_SKUS}; do
    log "  intentando SKU ${sku} (capacidad ${AZURE_FOUNDRY_MODEL_CAPACITY}K TPM) en ${LOCATION}"
    if deploy_err="$(az cognitiveservices account deployment create \
        --name "${AZURE_FOUNDRY_RESOURCE_NAME}" \
        --resource-group "${RESOURCE_GROUP}" \
        --deployment-name "${AZURE_FOUNDRY_DEPLOYMENT}" \
        --model-name "${AZURE_FOUNDRY_MODEL_NAME}" \
        --model-version "${AZURE_FOUNDRY_MODEL_VERSION}" \
        --model-format OpenAI \
        --sku-name "${sku}" \
        --sku-capacity "${AZURE_FOUNDRY_MODEL_CAPACITY}" 2>&1 >/dev/null)"; then
      log "  ✅ deployment creado con SKU ${sku}"
      deployed_sku="${sku}"
      break
    fi
    warn "  SKU ${sku} fallo: $(printf '%s' "${deploy_err}" | grep -i -m1 -E 'message|error|quota' || printf '%s' "${deploy_err}" | tail -1)"
  done
  if [ -z "${deployed_sku}" ]; then
    warn "No se pudo crear el deployment de ${AZURE_FOUNDRY_MODEL_NAME} con ningun SKU (${AZURE_FOUNDRY_MODEL_SKUS}) en ${LOCATION}."
    warn "Verifica tu cuota: az cognitiveservices usage list --location ${LOCATION} -o table"
  fi
fi

PROJECT_JSON="$(az_json cognitiveservices account project show \
  --name "${AZURE_FOUNDRY_RESOURCE_NAME}" \
  --resource-group "${RESOURCE_GROUP}" \
  --project-name "${AZURE_FOUNDRY_PROJECT}")"

FOUNDRY_ENDPOINT="$("${PYTHON_CMD}" -c 'import json,sys; data=json.load(sys.stdin); print(data.get("properties",{}).get("endpoint",""))' <<<"${PROJECT_JSON}")"
# El endpoint del proyecto a veces viene vacio: usa el del recurso (el que consume el SDK OpenAI).
if [ -z "${FOUNDRY_ENDPOINT//[$'\r\n']/}" ]; then
  FOUNDRY_ENDPOINT="$(az_tsv cognitiveservices account show \
    --name "${AZURE_FOUNDRY_RESOURCE_NAME}" \
    --resource-group "${RESOURCE_GROUP}" \
    --query "properties.endpoint")"
fi
FOUNDRY_KEY="$(az_tsv cognitiveservices account keys list \
  --name "${AZURE_FOUNDRY_RESOURCE_NAME}" \
  --resource-group "${RESOURCE_GROUP}" \
  --query key1)"
# Limpia retornos de carro (\r) que algunos entornos agregan y rompen la auth/URL.
FOUNDRY_ENDPOINT="${FOUNDRY_ENDPOINT//$'\r'/}"
FOUNDRY_KEY="${FOUNDRY_KEY//$'\r'/}"

set_output_var AZURE_FOUNDRY_RESOURCE_NAME "${AZURE_FOUNDRY_RESOURCE_NAME}"
set_output_var AZURE_FOUNDRY_PROJECT "${AZURE_FOUNDRY_PROJECT}"
set_output_var AZURE_FOUNDRY_ENDPOINT "${FOUNDRY_ENDPOINT}"
set_output_var AZURE_FOUNDRY_API_KEY "${FOUNDRY_KEY}"
set_output_var AZURE_FOUNDRY_DEPLOYMENT "${AZURE_FOUNDRY_DEPLOYMENT}"

log "Foundry listo"
