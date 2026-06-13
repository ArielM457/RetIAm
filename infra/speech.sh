#!/usr/bin/env bash
# Crea un recurso de Azure AI Speech (voz: TTS para narrar + STT para la voz del alumno).
# Intenta el tier GRATIS F0; si no se puede (ya tienes uno o no hay cupo), usa S0.
#
# Uso:
#   export RESOURCE_GROUP=retaim-rg
#   export LOCATION=eastus2
#   bash infra/speech.sh
#
# Nota: tu recurso de Foundry (kind AIServices) TAMBIÉN soporta Speech. Si prefieres no
# crear otro recurso, puedes reusar su key + region (ver el mensaje al final).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=infra/lib.sh
source "${SCRIPT_DIR}/lib.sh"

require_command az
PYTHON_CMD="$(detect_python_cmd)"

: "${RESOURCE_GROUP:?Define RESOURCE_GROUP}"
: "${LOCATION:?Define LOCATION}"

PROJECT_PREFIX="${PROJECT_PREFIX:-retaim}"
SUFFIX="${SUFFIX:-$(date '+%m%d%H%M')}"
SPEECH_NAME="${AZURE_SPEECH_NAME:-$(sanitize_name "${PROJECT_PREFIX}${SUFFIX}")speech}"

# Registra el provider si hace falta (idempotente).
state="$(az_tsv provider show --namespace Microsoft.CognitiveServices --query registrationState 2>/dev/null || true)"
[ "${state}" != "Registered" ] && { log "Registrando Microsoft.CognitiveServices"; az provider register --namespace Microsoft.CognitiveServices --wait >/dev/null; }

log "Creando recurso de Speech ${SPEECH_NAME}"
if ! az cognitiveservices account show --name "${SPEECH_NAME}" --resource-group "${RG:-$RESOURCE_GROUP}" >/dev/null 2>&1; then
  if az cognitiveservices account create \
       --name "${SPEECH_NAME}" --resource-group "${RESOURCE_GROUP}" \
       --kind SpeechServices --sku F0 --location "${LOCATION}" --yes >/dev/null 2>&1; then
    log "  ✅ creado en tier GRATIS F0"
  else
    warn "  F0 no disponible (¿ya tienes un F0?); usando S0 (pago por uso, barato)."
    az cognitiveservices account create \
      --name "${SPEECH_NAME}" --resource-group "${RESOURCE_GROUP}" \
      --kind SpeechServices --sku S0 --location "${LOCATION}" --yes >/dev/null
  fi
fi

SPEECH_KEY="$(az_tsv cognitiveservices account keys list \
  --name "${SPEECH_NAME}" --resource-group "${RESOURCE_GROUP}" --query key1)"
SPEECH_KEY="${SPEECH_KEY//$'\r'/}"
SPEECH_REGION="${LOCATION}"

set_output_var AZURE_SPEECH_NAME "${SPEECH_NAME}"
set_output_var AZURE_SPEECH_KEY "${SPEECH_KEY}"
set_output_var AZURE_SPEECH_REGION "${SPEECH_REGION}"

log "Speech listo. Agrega a server/.env (y/o al runtime-config del frontend):"
printf '  AZURE_SPEECH_KEY=%s\n' "${SPEECH_KEY}"
printf '  AZURE_SPEECH_REGION=%s\n' "${SPEECH_REGION}"
