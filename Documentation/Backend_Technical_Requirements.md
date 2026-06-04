# Requerimientos Tecnicos Externos

Este archivo lista lo que falta completar manualmente para que el backend funcione con servicios reales.

## 1. Supabase

Debes completar en `server/.env`:

- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`

Debes ejecutar `supabase/schema.sql` en tu proyecto real de Supabase.

Debes revisar en Supabase Auth:

- si la confirmacion por correo quedara activada o desactivada para la demo
- proveedores de login si mas adelante agregan uno real

## 2. Azure AI Foundry

Si quieres reemplazar el comportamiento mock por contenido fundamentado real, completa:

- `AZURE_FOUNDRY_ENDPOINT`
- `AZURE_FOUNDRY_PROJECT`
- `AZURE_FOUNDRY_DEPLOYMENT`
- `AZURE_FOUNDRY_API_KEY`
- `ENABLE_EXTERNAL_AI=true`

Con esto deberia conectarse la futura capa real de:

- generacion de rutas
- preguntas de aprendizaje
- examenes finales
- respuestas del agente

## 3. Azure AI Search y Blob Storage

Para una base de conocimiento real, completa:

- `AZURE_SEARCH_ENDPOINT`
- `AZURE_SEARCH_KEY`
- `AZURE_SEARCH_INDEX`
- `AZURE_BLOB_CONNECTION_STRING`

Esto es necesario para:

- indexar documentos sinteticos o reales
- servir contenido fundamentado para `Gini Path` y `Gini Eval`

## 4. Work IQ o Microsoft Graph

Para reemplazar el contexto mock de calendario, completa:

- `WORKIQ_TENANT_ID`
- `WORKIQ_CLIENT_ID`
- `WORKIQ_CLIENT_SECRET`

Esto permitiria:

- leer carga de reuniones
- estimar ventanas de foco
- ajustar recordatorios y planes semanales

## 5. Validacion tecnica

Cuando completes las variables, revisa:

- `GET /api/system/integrations/status`

Ese endpoint te mostrara si la configuracion base ya esta detectable desde backend.

## 6. Orden recomendado

1. Configurar Supabase y correr `schema.sql`
2. Probar auth y equipos
3. Probar onboarding y planes
4. Conectar Azure AI Foundry
5. Conectar Work IQ o Graph
