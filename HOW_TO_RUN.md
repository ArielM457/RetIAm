# Cómo correr RetAIM paso a paso (backend + frontend + IA real)

Guía a prueba de problemas para levantar el proyecto en local. Sigue las partes en orden.

> **Recomendación importante:** corre TODO desde una terminal de **WSL Ubuntu**, no desde
> PowerShell/CMD de Windows. El proyecto vive en el sistema de archivos de WSL
> (`/home/damon/proj-hack/RetIAm`) y el `npm` de Windows sobre `\\wsl.localhost` **crashea**
> ("Exit handler never called"). Desde WSL todo funciona nativo y sin fricción.
>
> Abre la terminal de Ubuntu (menú inicio → "Ubuntu") y empieza con:
> ```bash
> cd ~/proj-hack/RetIAm
> ```

**Orden de los pasos:** 1) Supabase (incl. pgvector) → 2) Backend → **3) IA real (Azure)** →
4) Levantar backend → 5) Cargar cursos → **5b) Poblar el RAG (`--rag`)** → 6) Frontend → 7) Probar.

---

## 0. Prerrequisitos

Dentro de WSL Ubuntu deberías tener:

```bash
python3 --version    # 3.11 o superior (probado con 3.14)
node -v              # 20 o superior (probado con 24)
npm -v               # 10 o superior
```

- Si `which npm` devuelve algo que empieza con `/mnt/c/...`, estás usando el npm de Windows.
  Abre una terminal de Ubuntu nueva para usar el de Linux.
- Necesitas una cuenta gratuita de **Supabase** (https://supabase.com).
- Para la IA real (paso 3) necesitas una **suscripción de Azure** con acceso a Azure OpenAI / Azure AI Foundry.

---

## 1. Supabase (base de datos + auth) — OBLIGATORIO

1. Crea un proyecto nuevo en https://supabase.com (plan free) y espera a que termine.
2. **SQL Editor → New query**, pega TODO el contenido de [`supabase/schema.sql`](supabase/schema.sql)
   y dale **Run**. Esto ya incluye el **RAG**: activa la extensión `vector` (pgvector), crea la
   tabla `lesson_chunks` (embeddings de 1024 dim), su índice HNSW y la función
   `match_lesson_chunks` que hace la búsqueda por similitud. No tienes que hacer nada extra en
   Supabase para el RAG.
3. **Project Settings → API**, copia:
   - **Project URL** → `SUPABASE_URL`
   - **anon public key** → `SUPABASE_ANON_KEY`
   - **service_role key** → `SUPABASE_SERVICE_ROLE_KEY` (secreto, solo backend)
4. **Authentication → Providers → Email** → **desactiva** "Confirm email" (Save).

---

## 2. Backend: instalar y configurar (todavía no lo levantamos)

Desde `~/proj-hack/RetIAm`:

```bash
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt     # openai (IA real), fastembed (embeddings RAG), beautifulsoup4 + markdownify (contenido legible)
cp .env.example .env
```

Abre `server/.env` y completa las llaves de Supabase del paso 1:

```env
SUPABASE_URL=https://TU_PROYECTO.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# Modelo de embeddings del RAG (local, gratis, CPU). Por defecto multilingual-e5-large (1024 dim).
# Normalmente NO necesitas tocar esto (ya tiene valor por defecto en el backend).
EMBEDDING_MODEL=intfloat/multilingual-e5-large
EMBEDDING_DIM=1024
```

> **¿Qué es esto del RAG?** El chat del tutor recupera fragmentos reales del contenido de las
> lecciones desde Supabase pgvector y se los pasa como contexto al modelo de Foundry. El modelo
> de embeddings (multilingual-e5-large) corre **local en tu CPU**, es gratis y NO es de Azure; Foundry solo
> redacta la respuesta final. Esto reemplaza a Azure AI Search (que cobra). Para que el tutor
> tenga material que recuperar, debes poblar el RAG en el **paso 5** (`--rag`).

> No levantes el backend todavía. Si vas a usar la IA real (recomendado para la hackathon),
> primero haz el **paso 3** para completar más variables del `.env`.

---

## 3. Activar la IA real con Azure (la parte de la hackathon) ⭐

Aquí es donde el tutor, los quizzes, el contenido y el examen pasan de modo mock a respuestas
**generadas y fundamentadas por los agentes Gini**. Mi backend solo necesita **un modelo
desplegado** (endpoint + key + nombre del deployment). NO necesitas crear los 8 agentes ni
Azure AI Search para que funcione la IA — eso es opcional.

> **Antes de empezar: registra el proveedor y verifica tu CUOTA.** Las suscripciones
> **Azure for Students** suelen traer cuota 0 para muchos modelos. Registra el proveedor (una vez
> por suscripción) y revisa qué tienes:
> ```bash
> az provider register --namespace Microsoft.CognitiveServices
> # cuota disponible (>0) por modelo+SKU en tu región:
> az cognitiveservices usage list --location eastus2 --query '[?limit>`0`].{Modelo:name.value, Limite:limit}' -o table
> ```
> Elige una región y un modelo/SKU con **Límite > 0**. En las cuentas de estudiante suele haber
> cuota en **`eastus2`** con SKU **`Standard`** (no `GlobalStandard`).

### Opción A — Portal de Azure (la más simple y confiable) ✅

1. Entra a https://ai.azure.com (Azure AI Foundry) o al portal de **Azure OpenAI**.
2. Crea un recurso (Azure AI Foundry / Azure OpenAI) en una región **con cupo**, p. ej. `eastus2`.
3. Ve a **Deployments → Deploy model** y despliega un modelo **vigente con cuota**, p. ej.
   **`gpt-4o` (versión `2024-11-20`)** con SKU **`Standard`**. Anota el **nombre del deployment**.
   ⚠️ Evita versiones deprecadas (p. ej. `gpt-4o-mini 2024-07-18` ya no se puede desplegar).
4. En **Keys and Endpoint** copia el **Endpoint** y una **Key**.
5. Completa en `server/.env`:

```env
ENABLE_EXTERNAL_AI=true
AZURE_FOUNDRY_ENDPOINT=https://TU-RECURSO.openai.azure.com/
AZURE_FOUNDRY_API_KEY=TU_KEY
AZURE_FOUNDRY_DEPLOYMENT=gpt-4o          # el NOMBRE del deployment del paso 3
AZURE_FOUNDRY_API_VERSION=2024-10-21
```

> El valor de `AZURE_FOUNDRY_DEPLOYMENT` debe ser EXACTAMENTE el nombre que le diste al
> deployment, no el del modelo si los cambiaste.

### Opción B — Por script (Azure CLI)

El script ya viene configurado para **`gpt-4o` versión `2024-11-20`** e intenta el SKU
**`Standard`** primero (con respaldo a `GlobalStandard`/`DataZoneStandard`):

```bash
az login
az group create --name retaim-rg --location eastus2
export RESOURCE_GROUP=retaim-rg
export LOCATION=eastus2
bash infra/foundry.sh        # crea/usa Foundry + despliega gpt-4o (Standard)
```

Deberías ver `✅ deployment creado con SKU Standard`. Si quieres otro modelo/versión/SKU, puedes
forzarlos sin tocar el script:
```bash
export AZURE_FOUNDRY_MODEL_NAME=gpt-4o AZURE_FOUNDRY_MODEL_VERSION=2024-11-20 AZURE_FOUNDRY_MODEL_SKU=Standard
export AZURE_FOUNDRY_DEPLOYMENT=gpt-4o   # nombre del deployment (= lo que va en .env)
```

Al terminar, lee los valores generados y cópialos a `server/.env`:

```bash
cat infra/.generated/provision.json   # AZURE_FOUNDRY_ENDPOINT, AZURE_FOUNDRY_API_KEY, AZURE_FOUNDRY_DEPLOYMENT
```

Pon también `ENABLE_EXTERNAL_AI=true` en `server/.env`.

### Grounding del tutor: RAG con Supabase pgvector (reemplaza a Azure AI Search)

El tutor se fundamenta (no inventa) recuperando fragmentos reales del contenido de las
lecciones desde **Supabase pgvector**, no desde Azure AI Search. Esto es **gratis** y ya quedó
configurado: la base vectorial vive en tu Supabase (paso 1) y el modelo de embeddings corre
local. Solo falta **poblarla**, lo cual se hace en el **paso 5** con la bandera `--rag`.

No necesitas `Azure AI Search` ni `knowledge_base.sh` para nada. Foundry recibe el texto de los
fragmentos ya recuperados; nunca ve la base vectorial directamente.

> Si NO quieres usar IA real, deja `ENABLE_EXTERNAL_AI=false`: el RAG sigue funcionando y el
> tutor responde de forma **extractiva** (te muestra el fragmento más relevante del material en
> vez de redactarlo con GPT-4o). Con Foundry activo, lo redacta y cita.

---

## 4. Levantar el backend

```bash
# (con el venv activado, dentro de server/)
uvicorn app.main:app --reload --port 8000
```

Verifica que la IA real quedó activa:

```bash
curl http://localhost:8000/api/health                       # -> {"status":"ok"}
curl http://localhost:8000/api/system/integrations/status   # -> "foundry_enabled": true
```

Si `foundry_enabled` es `true`, ¡la IA real está conectada! Docs de la API: http://localhost:8000/docs

> Deja esta terminal corriendo el backend.

---

## 5. Cargar los cursos (contenido real de Microsoft Learn)

En otra terminal, con el venv activado, desde la raíz del repo:

```bash
cd ~/proj-hack/RetIAm
source server/.venv/bin/activate

# Rápido (solo resúmenes): 50 cursos reales del catálogo
python infra/ingest_content.py --catalog --push

# Recomendado: 50 cursos CON el contenido completo legible que verá el estudiante
python infra/ingest_content.py --catalog --content --push
```

- **`--content`** baja el texto COMPLETO de cada lección desde Microsoft Learn y lo guarda como
  **Markdown legible** en `content_md` (es lo que el estudiante lee en la pantalla de la lección).
  Sin `--content`, la lección solo muestra el **resumen** + un link a la fuente.
- Si falla por SSL/certificado, agrega `--insecure-ssl`.
- Verifica: `curl http://localhost:8000/api/certifications` debe devolver muchos cursos.

### 5b. Poblar el RAG del tutor (recomendado) ⭐

Para que el chat del tutor pueda recuperar contenido real, agrega la bandera **`--rag`**. Esto
baja el **texto completo** de cada unidad de Microsoft Learn, lo trocea, genera los embeddings
(multilingual-e5-large, local) y los sube a la tabla `lesson_chunks` de Supabase. **`--rag` implica `--content`**,
así que con un solo comando obtienes el contenido legible del estudiante **y** el RAG del tutor
(una sola descarga, sin duplicar trabajo):

```bash
python infra/ingest_content.py --catalog --rag --push
```

> ⚠️ **La primera vez** fastembed **descarga el modelo de embeddings (~2 GB)** y luego procesa los 50
> cursos (descarga unidades + embeddings). Tarda **varios minutos**. Las siguientes veces el
> modelo ya está en caché. Es idempotente: re-correrlo reemplaza los chunks de cada lección.

- `--rag` requiere `--push` (necesita Supabase para guardar los vectores).
- Verifica en Supabase (**Table Editor → `lesson_chunks`**) que haya filas con `embedding`.
- El número de cursos lo ajustas con `--limit N` (por defecto 50).

---

## 6. Frontend (Angular)

En otra terminal de WSL, desde `~/proj-hack/RetIAm`:

```bash
cd client
npm install
cp public/runtime-config.example.js public/runtime-config.js
```

Edita `client/public/runtime-config.js` con tus datos de Supabase (los mismos del paso 1):

```js
window.__RETAIM_CONFIG__ = {
  apiBaseUrl: 'http://localhost:8000/api',
  supabaseUrl: 'https://TU_PROYECTO.supabase.co',
  supabaseAnonKey: 'eyJ...',   // anon public key
};
```

Levanta el frontend:

```bash
npx ng serve
```

Abre **http://localhost:4200**.

---

## 7. Probar el recorrido completo (y confirmar que la IA funciona)

1. **Crear cuenta** en /login.
2. **Onboarding**: responde la evaluación inicial.
3. **Cursos** (/catalog): abre un curso → **"Generar mi ruta y plan"**.
4. **Sesiones** (/sessions): entra a una sección, abre el **tutor IA** y hazle una pregunta
   sobre la lección. Responde el **quiz** y completa lecciones.
5. **Examen** (/exam) y **Certificados** (/certificates).

**Cómo saber si la IA real está respondiendo (no el mock):**
- En el chat del tutor, las respuestas del backend traen `source_mode: "foundry"` (mock cuando
  está apagado). Lo ves en la pestaña **Network** del navegador, en la respuesta de
  `.../lessons/.../chat`.
- `GET /api/system/integrations/status` muestra `foundry_enabled: true`.
- Las respuestas del tutor y los quizzes son contextuales (no plantillas fijas).

**Cómo saber si el RAG está funcionando:**
- Las respuestas del tutor traen `sources` con `source: "rag"` y la URL de Microsoft Learn de
  donde salió el fragmento.
- Si el tutor responde *"No encuentro material indexado…"*, es que **no corriste el paso 5b**
  (`--rag`) o esa certificación no se ingirió con RAG.

---

## 8. Solución de problemas

| Síntoma | Causa / Solución |
|--------|------------------|
| `npm error Exit handler never called` | Estás usando el npm de Windows sobre `\\wsl.localhost`. **Corre desde una terminal de WSL Ubuntu**. |
| `which npm` muestra `/mnt/c/...` | Es el npm de Windows. Abre una terminal Ubuntu nueva. |
| `email-validator is not installed` | `pip install -r requirements.txt` con el venv activado. |
| `foundry_enabled` sale `false` | Falta alguna de: `ENABLE_EXTERNAL_AI=true`, `AZURE_FOUNDRY_ENDPOINT`, `AZURE_FOUNDRY_API_KEY`, `AZURE_FOUNDRY_DEPLOYMENT`. Reinicia uvicorn tras editar `.env`. |
| El tutor responde pero con `source_mode: "mock"` | La llamada a Foundry falló y cayó al fallback. Revisa que el **nombre del deployment** y la `AZURE_FOUNDRY_API_VERSION` sean correctos; mira los logs del backend (imprime el warning del error de Foundry). |
| Error 401/403 desde Foundry | Key o endpoint incorrectos, o el recurso no tiene el modelo desplegado con ese nombre. |
| `DeploymentNotFound` | `AZURE_FOUNDRY_DEPLOYMENT` no coincide con el nombre real del deployment en Azure. |
| `MissingSubscriptionRegistration ... Microsoft.CognitiveServices` | Registra el proveedor (una vez): `az provider register --namespace Microsoft.CognitiveServices` y espera a `Registered`. |
| `InsufficientQuota ... quota limit is 0` | No tienes cuota para ese modelo+SKU+región. Revisa con `az cognitiveservices usage list --location <region> --query '[?limit>\`0\`]' -o table` y usa una combinación con Límite > 0 (en Student suele ser `eastus2` + `Standard`). |
| `ServiceModelDeprecated ... has been deprecated` | La versión del modelo ya no se puede desplegar. Usa una vigente (p. ej. `gpt-4o` `2024-11-20`). Ver versiones: `az cognitiveservices account list-models --name <recurso> -g <rg> --query "[?name=='gpt-4o'].version"`. |
| La ingesta falla con error SSL | Agrega `--insecure-ssl`. |
| El tutor dice "No encuentro material indexado" | No corriste la ingesta con `--rag` (paso 5b), o esa certificación no se ingirió. Corre `python infra/ingest_content.py --catalog --rag --push`. |
| La ingesta `--rag` "se cuelga" al inicio | Está descargando el modelo de embeddings (~2 GB) la primera vez. Espera; es normal. |
| `Could not find a version that satisfies fastembed` | Tu Python es 3.13+. Ya está como `fastembed>=0.5.0` en requirements; corre de nuevo `pip install -r requirements.txt`. |
| `ModuleNotFoundError: fastembed` | `pip install -r requirements.txt` con el venv activado. |
| `ModuleNotFoundError: bs4` / `markdownify` | Igual: `pip install -r requirements.txt`. Sin ellos, `--content` cae a texto plano (sin formato Markdown). |
| La lección muestra solo el resumen + un link | No corriste la ingesta con `--content` (o `--rag`). Corre `python infra/ingest_content.py --catalog --content --push`. |
| `function match_lesson_chunks does not exist` o `type vector does not exist` | No corriste el `schema.sql` actualizado (paso 1.2) que activa pgvector. Vuelve a ejecutarlo. |
| `lesson_chunks` está vacía tras `--rag` | Faltó `--push` (el RAG requiere Supabase), o falló el embedding/descarga de unidades; revisa los logs. |
| Frontend: "Missing runtime config" / "placeholders" | No completaste `client/public/runtime-config.js` con tus datos reales. |
| Errores de CORS | El backend permite `http://localhost:4200`. Si cambiaste el puerto, ajusta `CLIENT_URL` en `server/.env`. |
| `/api/certifications` devuelve solo 4 | Aún no corriste la ingesta con `--push` (paso 5). |
| El examen dice "completa todas las secciones" | Correcto: completa las secciones del plan antes del examen. |
| Login pide confirmar correo | Desactiva "Confirm email" en Supabase (paso 1.4). |

---

## Resumen de puertos y URLs

- Backend API: **http://localhost:8000** (docs `/docs`, health `/api/health`, estado IA `/api/system/integrations/status`)
- Frontend: **http://localhost:4200**
- El frontend habla con el backend vía `apiBaseUrl` (`http://localhost:8000/api`).

---

## Nota de costos (Azure)

- El modelo `gpt-4o` se cobra por uso (el consumo de una demo es mínimo; con cuota de estudiante en
  `Standard` basta y sobra). `gpt-4o-mini` sería aún más barato, pero su versión vigente puede no
  tener cuota en tu suscripción — por eso el script usa `gpt-4o`.
- El **RAG es gratis**: pgvector va en Supabase (free) y los embeddings (multilingual-e5-large) corren local en
  tu CPU. **No usamos Azure AI Search** (eso era lo que cobraba).
- Al terminar la demo, puedes borrar todo con `bash infra/cleanup.sh` para no dejar recursos.
