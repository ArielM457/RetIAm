#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-${SCRIPT_DIR}/.generated}"
OUTPUT_ENV_FILE="${OUTPUT_ENV_FILE:-${OUTPUT_DIR}/provision.env}"
OUTPUT_JSON_FILE="${OUTPUT_JSON_FILE:-${OUTPUT_DIR}/provision.json}"

mkdir -p "${OUTPUT_DIR}"

log() {
  printf '\n[%s] %s\n' "$(date '+%H:%M:%S')" "$*"
}

warn() {
  printf '\n[WARN] %s\n' "$*" >&2
}

fail() {
  printf '\n[ERROR] %s\n' "$*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "Falta el comando requerido: $1"
}

detect_python_cmd() {
  if [[ -n "${PYTHON_CMD:-}" ]] && command -v "${PYTHON_CMD}" >/dev/null 2>&1; then
    echo "${PYTHON_CMD}"
    return
  fi

  if command -v python3 >/dev/null 2>&1; then
    echo "python3"
    return
  fi

  if command -v python >/dev/null 2>&1; then
    echo "python"
    return
  fi

  fail "No se encontro python3 ni python en el entorno actual."
}

ensure_file() {
  local file_path="$1"
  [[ -f "${file_path}" ]] || fail "No existe el archivo requerido: ${file_path}"
}

sanitize_name() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9'
}

load_optional_env_file() {
  local env_file="${1:-}"
  if [[ -n "${env_file}" && -f "${env_file}" ]]; then
    log "Cargando variables desde ${env_file}"
    set -a
    # shellcheck disable=SC1090
    source "${env_file}"
    set +a
  fi
}

az_json() {
  az "$@" -o json
}

az_tsv() {
  az "$@" -o tsv
}

set_output_var() {
  local key="$1"
  local value="${2:-}"
  export "${key}=${value}"

  "${PYTHON_CMD}" - "${OUTPUT_JSON_FILE}" "${key}" "${value}" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
key = sys.argv[2]
value = sys.argv[3]

data = {}
if path.exists():
    data = json.loads(path.read_text(encoding="utf-8"))
data[key] = value
path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
PY
}

render_env_file() {
  : >"${OUTPUT_ENV_FILE}"
  local keys=(
    RESOURCE_GROUP
    LOCATION
    AZURE_SUBSCRIPTION_ID
    AZURE_FOUNDRY_RESOURCE_NAME
    AZURE_FOUNDRY_PROJECT
    AZURE_FOUNDRY_ENDPOINT
    AZURE_FOUNDRY_API_KEY
    AZURE_FOUNDRY_DEPLOYMENT
    AZURE_SEARCH_SERVICE
    AZURE_SEARCH_ENDPOINT
    AZURE_SEARCH_INDEX
    AZURE_SEARCH_KEY
    AZURE_STORAGE_ACCOUNT
    AZURE_BLOB_CONTAINER
    AZURE_BLOB_CONNECTION_STRING
    CONTAINERAPPS_ENVIRONMENT
    BACKEND_CONTAINER_APP
    BACKEND_CONTAINER_APP_URL
    STATIC_WEB_APP
    STATIC_WEB_APP_URL
    GINI_ROUTER_ID
    GINI_PROFILE_ID
    GINI_PATH_ID
    GINI_PLANNER_ID
    GINI_COACH_ID
    GINI_EVAL_ID
    GINI_INSIGHT_ID
    GINI_LENS_ID
  )

  for key in "${keys[@]}"; do
    if [[ -n "${!key:-}" ]]; then
      printf '%s=%q\n' "${key}" "${!key}" >>"${OUTPUT_ENV_FILE}"
    fi
  done
}

register_resource_providers() {
  local providers=(
    Microsoft.App
    Microsoft.OperationalInsights
    Microsoft.CognitiveServices
    Microsoft.Search
    Microsoft.Storage
    Microsoft.Web
  )

  for provider in "${providers[@]}"; do
    local state
    state="$(az_tsv provider show --namespace "${provider}" --query registrationState 2>/dev/null || true)"
    if [[ "${state}" != "Registered" ]]; then
      log "Registrando provider ${provider}"
      az provider register --namespace "${provider}" --wait >/dev/null
    fi
  done
}
