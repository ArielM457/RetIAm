#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=infra/lib.sh
source "${SCRIPT_DIR}/lib.sh"

require_command az
require_command curl
PYTHON_CMD="$(detect_python_cmd)"

: "${RESOURCE_GROUP:?Debes definir RESOURCE_GROUP}"
: "${LOCATION:?Debes definir LOCATION}"

PROJECT_PREFIX="${PROJECT_PREFIX:-retaim}"
SUFFIX="${SUFFIX:-$(date '+%m%d%H%M')}"
BASE_NAME="$(sanitize_name "${PROJECT_PREFIX}${SUFFIX}")"

AZURE_SEARCH_SERVICE="${AZURE_SEARCH_SERVICE:-${BASE_NAME}search}"
AZURE_SEARCH_INDEX="${AZURE_SEARCH_INDEX:-retaim-knowledge}"
AZURE_STORAGE_ACCOUNT="${AZURE_STORAGE_ACCOUNT:-${BASE_NAME}blob}"
AZURE_BLOB_CONTAINER="${AZURE_BLOB_CONTAINER:-certifications}"
SEARCH_API_VERSION="${SEARCH_API_VERSION:-2024-07-01}"
CERTIFICATIONS_DIR="${CERTIFICATIONS_DIR:-${REPO_ROOT}/synthetic-data/certifications}"

log "Creando Azure AI Search ${AZURE_SEARCH_SERVICE}"
if ! az search service show --name "${AZURE_SEARCH_SERVICE}" --resource-group "${RESOURCE_GROUP}" >/dev/null 2>&1; then
  az search service create \
    --name "${AZURE_SEARCH_SERVICE}" \
    --resource-group "${RESOURCE_GROUP}" \
    --location "${LOCATION}" \
    --sku basic \
    --partition-count 1 \
    --replica-count 1 >/dev/null
fi

AZURE_SEARCH_KEY="$(az_tsv search service admin-key list \
  --search-service-name "${AZURE_SEARCH_SERVICE}" \
  --resource-group "${RESOURCE_GROUP}" \
  --query primaryKey)"
AZURE_SEARCH_ENDPOINT="https://${AZURE_SEARCH_SERVICE}.search.windows.net"

log "Creando Storage Account ${AZURE_STORAGE_ACCOUNT}"
if ! az storage account show --name "${AZURE_STORAGE_ACCOUNT}" --resource-group "${RESOURCE_GROUP}" >/dev/null 2>&1; then
  az storage account create \
    --name "${AZURE_STORAGE_ACCOUNT}" \
    --resource-group "${RESOURCE_GROUP}" \
    --location "${LOCATION}" \
    --sku Standard_LRS \
    --kind StorageV2 \
    --min-tls-version TLS1_2 \
    --allow-blob-public-access false >/dev/null
fi

AZURE_BLOB_CONNECTION_STRING="$(az_tsv storage account show-connection-string \
  --name "${AZURE_STORAGE_ACCOUNT}" \
  --resource-group "${RESOURCE_GROUP}" \
  --query connectionString)"

log "Creando contenedor ${AZURE_BLOB_CONTAINER}"
az storage container create \
  --name "${AZURE_BLOB_CONTAINER}" \
  --connection-string "${AZURE_BLOB_CONNECTION_STRING}" >/dev/null

if [[ -d "${CERTIFICATIONS_DIR}" ]] && find "${CERTIFICATIONS_DIR}" -type f | read -r _; then
  log "Subiendo documentos desde ${CERTIFICATIONS_DIR}"
  az storage blob upload-batch \
    --connection-string "${AZURE_BLOB_CONNECTION_STRING}" \
    --destination "${AZURE_BLOB_CONTAINER}" \
    --source "${CERTIFICATIONS_DIR}" \
    --overwrite >/dev/null
else
  warn "No hay archivos en ${CERTIFICATIONS_DIR}. Se crea la infraestructura pero el contenedor queda vacio."
fi

create_search_object() {
  local kind="$1"
  local name="$2"
  local payload="$3"
  curl -fsS -X PUT \
    "${AZURE_SEARCH_ENDPOINT}/${kind}/${name}?api-version=${SEARCH_API_VERSION}" \
    -H "Content-Type: application/json" \
    -H "api-key: ${AZURE_SEARCH_KEY}" \
    --data "${payload}" >/dev/null
}

log "Creando indice y pipeline de indexacion"
create_search_object "indexes" "${AZURE_SEARCH_INDEX}" '{
  "name": "'"${AZURE_SEARCH_INDEX}"'",
  "fields": [
    { "name": "id", "type": "Edm.String", "key": true, "searchable": false, "filterable": true, "sortable": false, "facetable": false },
    { "name": "content", "type": "Edm.String", "searchable": true, "retrievable": true, "analyzer": "es.microsoft" },
    { "name": "title", "type": "Edm.String", "searchable": true, "retrievable": true },
    { "name": "path", "type": "Edm.String", "searchable": false, "retrievable": true, "filterable": true },
    { "name": "category", "type": "Edm.String", "searchable": true, "retrievable": true, "filterable": true }
  ]
}'

DATASOURCE_NAME="${AZURE_SEARCH_INDEX}-blob-ds"
INDEXER_NAME="${AZURE_SEARCH_INDEX}-blob-indexer"

create_search_object "datasources" "${DATASOURCE_NAME}" '{
  "name": "'"${DATASOURCE_NAME}"'",
  "type": "azureblob",
  "credentials": {
    "connectionString": "'"${AZURE_BLOB_CONNECTION_STRING}"'"
  },
  "container": {
    "name": "'"${AZURE_BLOB_CONTAINER}"'"
  }
}'

create_search_object "indexers" "${INDEXER_NAME}" '{
  "name": "'"${INDEXER_NAME}"'",
  "dataSourceName": "'"${DATASOURCE_NAME}"'",
  "targetIndexName": "'"${AZURE_SEARCH_INDEX}"'",
  "parameters": {
    "configuration": {
      "dataToExtract": "contentAndMetadata",
      "parsingMode": "default"
    }
  },
  "fieldMappings": [
    { "sourceFieldName": "metadata_storage_path", "targetFieldName": "id", "mappingFunction": { "name": "base64Encode" } },
    { "sourceFieldName": "metadata_storage_name", "targetFieldName": "title" },
    { "sourceFieldName": "metadata_storage_path", "targetFieldName": "path" }
  ],
  "outputFieldMappings": []
}'

curl -fsS -X POST \
  "${AZURE_SEARCH_ENDPOINT}/indexers/${INDEXER_NAME}/run?api-version=${SEARCH_API_VERSION}" \
  -H "api-key: ${AZURE_SEARCH_KEY}" >/dev/null || warn "No se pudo disparar el indexer automaticamente. Revisa el servicio de Search."

set_output_var AZURE_SEARCH_SERVICE "${AZURE_SEARCH_SERVICE}"
set_output_var AZURE_SEARCH_ENDPOINT "${AZURE_SEARCH_ENDPOINT}"
set_output_var AZURE_SEARCH_INDEX "${AZURE_SEARCH_INDEX}"
set_output_var AZURE_SEARCH_KEY "${AZURE_SEARCH_KEY}"
set_output_var AZURE_STORAGE_ACCOUNT "${AZURE_STORAGE_ACCOUNT}"
set_output_var AZURE_BLOB_CONTAINER "${AZURE_BLOB_CONTAINER}"
set_output_var AZURE_BLOB_CONNECTION_STRING "${AZURE_BLOB_CONNECTION_STRING}"

log "Knowledge base lista"
