# Backend Epica 8

## Objetivo

Preparar la capa backend para integraciones externas y automatizacion de infraestructura.

## Endpoints

- `GET /api/system/integrations/status`

## Notas para frontend

- Esta épica no define pantallas centrales de usuario final, pero el frontend puede usar `integrations/status` para mostrar un panel de estado tecnico si el equipo lo necesita.
- El backend ya tiene adaptadores y variables de entorno preparadas para:
- Supabase
- Azure AI Foundry
- Azure AI Search
- Azure Blob Storage
- Work IQ o Microsoft Graph

## Archivos tecnicos relevantes

- `server/.env.example`
- `server/app/integrations/foundry_adapter.py`
- `server/app/integrations/workiq_adapter.py`
- `infra/provision.sh`
- `Documentation/Backend_Technical_Requirements.md`
