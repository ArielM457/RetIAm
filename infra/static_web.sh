#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=infra/lib.sh
source "${SCRIPT_DIR}/lib.sh"

require_command az

: "${RESOURCE_GROUP:?Debes definir RESOURCE_GROUP}"

STATIC_WEB_APP="${STATIC_WEB_APP:-retaim-web}"
STATIC_WEB_APP_SKU="${STATIC_WEB_APP_SKU:-Free}"

if ! az staticwebapp show --name "${STATIC_WEB_APP}" --resource-group "${RESOURCE_GROUP}" >/dev/null 2>&1; then
  log "Creando Static Web App ${STATIC_WEB_APP}"
  if [[ -n "${STATIC_WEB_APP_SOURCE:-}" && -n "${STATIC_WEB_APP_BRANCH:-}" ]]; then
    token_args=()
    if [[ -n "${STATIC_WEB_APP_TOKEN:-}" ]]; then
      token_args=(--token "${STATIC_WEB_APP_TOKEN}")
    fi

    az staticwebapp create \
      --name "${STATIC_WEB_APP}" \
      --resource-group "${RESOURCE_GROUP}" \
      --location "${LOCATION:-centralus}" \
      --source "${STATIC_WEB_APP_SOURCE}" \
      --branch "${STATIC_WEB_APP_BRANCH}" \
      --app-location "${STATIC_WEB_APP_APP_LOCATION:-/client}" \
      --output-location "${STATIC_WEB_APP_OUTPUT_LOCATION:-dist/client/browser}" \
      --sku "${STATIC_WEB_APP_SKU}" \
      "${token_args[@]}" >/dev/null
  else
    az staticwebapp create \
      --name "${STATIC_WEB_APP}" \
      --resource-group "${RESOURCE_GROUP}" \
      --location "${LOCATION:-centralus}" \
      --sku "${STATIC_WEB_APP_SKU}" >/dev/null
  fi
fi

STATIC_WEB_APP_URL="$(az_tsv staticwebapp show \
  --name "${STATIC_WEB_APP}" \
  --resource-group "${RESOURCE_GROUP}" \
  --query defaultHostname)"

set_output_var STATIC_WEB_APP "${STATIC_WEB_APP}"
set_output_var STATIC_WEB_APP_URL "https://${STATIC_WEB_APP_URL}"

log "Static Web App lista"
