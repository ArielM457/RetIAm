# Infraestructura Azure

Esta carpeta implementa la epica 8 del repo: aprovisionamiento automatizado de Azure con Azure CLI y helpers para validar el backend.

## Scripts principales

- `provision.sh`
- `foundry.sh`
- `knowledge_base.sh`
- `container_apps.sh`
- `static_web.sh`
- `cleanup.sh`
- `validate_setup.py`

## Que crea `provision.sh`

1. Resource Group
2. Recurso de Microsoft Foundry y project
3. Azure AI Search
4. Azure Blob Storage y contenedor para documentos
5. Indice, datasource e indexer en Search
6. Azure Container Apps environment y backend app
7. Azure Static Web App
8. Agentes Gini por Python SDK

## Uso rapido

```bash
az login
bash infra/provision.sh
```

Tambien puedes pasar un archivo `.env` de infraestructura:

```bash
bash infra/provision.sh infra/dev.env
```

Variables utiles opcionales:

- `RESOURCE_GROUP`
- `LOCATION`
- `PROJECT_PREFIX`
- `BACKEND_IMAGE`
- `STATIC_WEB_APP_SOURCE`
- `STATIC_WEB_APP_BRANCH`
- `STATIC_WEB_APP_TOKEN`
- `SKIP_AGENTS`

Al finalizar se genera `infra/.generated/provision.env` con endpoints y valores exportables.

## Variables de Supabase

El provisioning de Azure no crea Supabase. Estas variables salen de tu proyecto de Supabase y debes copiarlas manualmente:

- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`

Para el frontend, `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` normalmente corresponde a la misma clave publica que aqui llamamos `SUPABASE_ANON_KEY`.

## Validacion backend

```powershell
cd server
.\.venv\Scripts\python ..\infra\validate_setup.py
```
