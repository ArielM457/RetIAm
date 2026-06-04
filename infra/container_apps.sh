#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=infra/lib.sh
source "${SCRIPT_DIR}/lib.sh"

require_command az

: "${RESOURCE_GROUP:?Debes definir RESOURCE_GROUP}"
: "${LOCATION:?Debes definir LOCATION}"

CONTAINERAPPS_ENVIRONMENT="${CONTAINERAPPS_ENVIRONMENT:-retaim-env}"
BACKEND_CONTAINER_APP="${BACKEND_CONTAINER_APP:-retaim-api}"
LOG_ANALYTICS_WORKSPACE="${LOG_ANALYTICS_WORKSPACE:-retaim-logs}"
BACKEND_IMAGE="${BACKEND_IMAGE:-mcr.microsoft.com/azuredocs/containerapps-helloworld:latest}"
BACKEND_TARGET_PORT="${BACKEND_TARGET_PORT:-8000}"

log "Creando Log Analytics ${LOG_ANALYTICS_WORKSPACE}"
if ! az monitor log-analytics workspace show --resource-group "${RESOURCE_GROUP}" --workspace-name "${LOG_ANALYTICS_WORKSPACE}" >/dev/null 2>&1; then
  az monitor log-analytics workspace create \
    --resource-group "${RESOURCE_GROUP}" \
    --workspace-name "${LOG_ANALYTICS_WORKSPACE}" \
    --location "${LOCATION}" >/dev/null
fi

WORKSPACE_ID="$(az_tsv monitor log-analytics workspace show \
  --resource-group "${RESOURCE_GROUP}" \
  --workspace-name "${LOG_ANALYTICS_WORKSPACE}" \
  --query customerId)"
WORKSPACE_KEY="$(az_tsv monitor log-analytics workspace get-shared-keys \
  --resource-group "${RESOURCE_GROUP}" \
  --workspace-name "${LOG_ANALYTICS_WORKSPACE}" \
  --query primarySharedKey)"

log "Creando Container Apps environment ${CONTAINERAPPS_ENVIRONMENT}"
if ! az containerapp env show --name "${CONTAINERAPPS_ENVIRONMENT}" --resource-group "${RESOURCE_GROUP}" >/dev/null 2>&1; then
  az containerapp env create \
    --name "${CONTAINERAPPS_ENVIRONMENT}" \
    --resource-group "${RESOURCE_GROUP}" \
    --location "${LOCATION}" \
    --logs-workspace-id "${WORKSPACE_ID}" \
    --logs-workspace-key "${WORKSPACE_KEY}" >/dev/null
fi

ENV_VARS=(
  "APP_ENV=production"
  "CLIENT_URL=${STATIC_WEB_APP_URL:-https://example.com}"
)

for name in \
  SUPABASE_URL SUPABASE_ANON_KEY SUPABASE_SERVICE_ROLE_KEY \
  AZURE_FOUNDRY_ENDPOINT AZURE_FOUNDRY_PROJECT AZURE_FOUNDRY_DEPLOYMENT AZURE_FOUNDRY_API_KEY \
  AZURE_SEARCH_ENDPOINT AZURE_SEARCH_KEY AZURE_SEARCH_INDEX AZURE_BLOB_CONNECTION_STRING \
  WORKIQ_TENANT_ID WORKIQ_CLIENT_ID WORKIQ_CLIENT_SECRET ENABLE_EXTERNAL_AI; do
  if [[ -n "${!name:-}" ]]; then
    ENV_VARS+=("${name}=${!name}")
  fi
done

log "Creando Container App ${BACKEND_CONTAINER_APP}"
if ! az containerapp show --name "${BACKEND_CONTAINER_APP}" --resource-group "${RESOURCE_GROUP}" >/dev/null 2>&1; then
  az containerapp create \
    --name "${BACKEND_CONTAINER_APP}" \
    --resource-group "${RESOURCE_GROUP}" \
    --environment "${CONTAINERAPPS_ENVIRONMENT}" \
    --image "${BACKEND_IMAGE}" \
    --target-port "${BACKEND_TARGET_PORT}" \
    --ingress external \
    --min-replicas 1 \
    --max-replicas 1 \
    --env-vars "${ENV_VARS[@]}" >/dev/null
else
  az containerapp update \
    --name "${BACKEND_CONTAINER_APP}" \
    --resource-group "${RESOURCE_GROUP}" \
    --image "${BACKEND_IMAGE}" \
    --set-env-vars "${ENV_VARS[@]}" >/dev/null
fi

BACKEND_CONTAINER_APP_URL="$(az_tsv containerapp show \
  --name "${BACKEND_CONTAINER_APP}" \
  --resource-group "${RESOURCE_GROUP}" \
  --query properties.configuration.ingress.fqdn)"

set_output_var CONTAINERAPPS_ENVIRONMENT "${CONTAINERAPPS_ENVIRONMENT}"
set_output_var BACKEND_CONTAINER_APP "${BACKEND_CONTAINER_APP}"
set_output_var BACKEND_CONTAINER_APP_URL "https://${BACKEND_CONTAINER_APP_URL}"

log "Container Apps listo"
