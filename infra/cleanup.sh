#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=infra/lib.sh
source "${SCRIPT_DIR}/lib.sh"

require_command az

: "${RESOURCE_GROUP:?Debes definir RESOURCE_GROUP}"

log "Eliminando resource group ${RESOURCE_GROUP}"
az group delete --name "${RESOURCE_GROUP}" --yes --no-wait
log "Limpieza lanzada. Azure seguira borrando recursos en segundo plano."
