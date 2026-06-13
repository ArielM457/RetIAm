#!/usr/bin/env bash
# Despliega modelos extra (gpt-4.1-mini para la Sala 1, gpt-4.1 para supervision)
# en el recurso de Foundry que YA tienes. Auto-detecta version vigente y SKU con cuota
# (prueba Standard -> GlobalStandard -> DataZoneStandard, y salta versiones deprecadas).
#
# Uso:
#   export RESOURCE_GROUP=retaim-rg
#   export LOCATION=eastus2
#   export AZURE_FOUNDRY_RESOURCE_NAME=retaim06052203foundry   # tu recurso existente
#   bash infra/deploy_models.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=infra/lib.sh
source "${SCRIPT_DIR}/lib.sh"

require_command az
PYTHON_CMD="$(detect_python_cmd)"

: "${RESOURCE_GROUP:?Define RESOURCE_GROUP}"
: "${LOCATION:?Define LOCATION}"
: "${AZURE_FOUNDRY_RESOURCE_NAME:?Define AZURE_FOUNDRY_RESOURCE_NAME (tu recurso de Foundry existente)}"

RES="${AZURE_FOUNDRY_RESOURCE_NAME}"
RG="${RESOURCE_GROUP}"
CAP="${MODEL_CAPACITY:-10}"           # 10 = 10K TPM por deployment
SKUS="${MODEL_SKUS:-Standard GlobalStandard DataZoneStandard}"

# Modelos a desplegar: "modelo:nombre_deployment". Editable con MODELS="...".
MODELS="${MODELS:-gpt-4.1-mini:gpt-4.1-mini gpt-4.1:gpt-4.1}"

log "Cuota disponible (>0) de gpt-4.1* en ${LOCATION}:"
az cognitiveservices usage list --location "${LOCATION}" \
  --query "[?contains(name.value,'gpt-4.1') && limit>\`0\`].{Cuota:name.value, Limite:limit, Uso:currentValue}" \
  -o table || true

deploy_one() {
  local model="$1" deployment="$2"

  if az cognitiveservices account deployment show \
       --name "${RES}" --resource-group "${RG}" --deployment-name "${deployment}" >/dev/null 2>&1; then
    log "  '${deployment}' ya existe; lo dejo como está."
    return 0
  fi

  local versions
  # tr -d '\r': el az de Windows (vía interop WSL) añade CR en la salida TSV,
  # y ese \r corrompe la versión al desplegar (DeploymentModelNotSupported).
  versions="$(az cognitiveservices account list-models --name "${RES}" --resource-group "${RG}" \
    --query "[?name=='${model}'].version" -o tsv 2>/dev/null | tr -d '\r' | sort -r)"
  if [ -z "${versions}" ]; then
    warn "  '${model}' no está disponible para desplegar en este recurso/región."
    return 1
  fi

  local v s
  for v in ${versions}; do
    for s in ${SKUS}; do
      if az cognitiveservices account deployment create \
           --name "${RES}" --resource-group "${RG}" \
           --deployment-name "${deployment}" \
           --model-name "${model}" --model-version "${v}" \
           --model-format OpenAI --sku-name "${s}" --sku-capacity "${CAP}" >/dev/null 2>&1; then
        log "  ✅ ${deployment} = ${model} v${v} (SKU ${s}, ${CAP}K TPM)"
        return 0
      fi
    done
  done
  warn "  ❌ No se pudo desplegar '${model}': sin cuota o todas las versiones deprecadas."
  return 1
}

PRESENTER=""
SUPERVISOR=""
for pair in ${MODELS}; do
  model="${pair%%:*}"
  deployment="${pair##*:}"
  log "Desplegando ${model} (deployment ${deployment})"
  if deploy_one "${model}" "${deployment}"; then
    case "${model}" in
      gpt-4.1-mini) PRESENTER="${deployment}" ;;
      gpt-4.1)      SUPERVISOR="${deployment}" ;;
    esac
  fi
done

[ -n "${PRESENTER}" ]  && set_output_var AZURE_FOUNDRY_DEPLOYMENT_PRESENTER  "${PRESENTER}"
[ -n "${SUPERVISOR}" ] && set_output_var AZURE_FOUNDRY_DEPLOYMENT_SUPERVISOR "${SUPERVISOR}"

log "Listo. Agrega a server/.env lo que se haya desplegado:"
[ -n "${PRESENTER}" ]  && printf '  AZURE_FOUNDRY_DEPLOYMENT_PRESENTER=%s\n'  "${PRESENTER}"
[ -n "${SUPERVISOR}" ] && printf '  AZURE_FOUNDRY_DEPLOYMENT_SUPERVISOR=%s\n' "${SUPERVISOR}"
[ -z "${PRESENTER}${SUPERVISOR}" ] && warn "No se desplegó ningún 4.1. Revisa cuota; mientras, la app usa gpt-4o."
