# Progress

## 2026-06-01

### Lo que hicimos hoy

- Inicializamos `server` con `FastAPI` y una estructura base en `app/api`, `app/core`, `app/db`, `app/models` y `app/services`.
- Dejamos configurada la conexion a Supabase para auth y base de datos desde backend.
- Agregamos validacion de correo para el MVP de la hackathon.
- Creamos el endpoint `GET /api/health`.
- Creamos el endpoint `POST /api/auth/validate-email`.
- Creamos el endpoint `GET /api/users/me` para sincronizar y leer el perfil autenticado.
- Inicializamos `client` con `Angular`.
- Configuramos `Tailwind CSS` en el frontend.
- Configuramos `Supabase Auth` en el frontend con flujo de login y registro.
- Dejamos un dashboard inicial protegido por sesion.
- Agregamos `supabase/schema.sql` con tablas base para organizaciones, perfiles, equipos y miembros.
- Agregamos `.gitignore` y ejemplos de configuracion para que el repo quede listo para subir.

## 2026-06-02

### Lo que hicimos hoy en backend

- Cerramos la base de la Épica 1 en `server`.
- El backend ahora acepta cualquier correo valido para la demo.
- Si el correo usa un dominio publico como `gmail.com`, el sistema recomienda usar un dominio institucional o del equipo, pero no bloquea el acceso.
- Agregamos `POST /api/auth/register` para crear usuarios mock en Supabase y devolver sesion.
- Agregamos `POST /api/auth/login` para iniciar sesion contra Supabase y devolver tokens.
- Extendimos `POST /api/auth/validate-email` para devolver recomendacion y clasificacion del dominio.
- Agregamos `PATCH /api/users/me` para actualizar el perfil base.
- Agregamos rutas de equipos:
- `GET /api/teams`
- `POST /api/teams`
- `GET /api/teams/{team_id}/members`
- `POST /api/teams/{team_id}/invites`
- `GET /api/teams/invitations/mine`
- `POST /api/teams/invitations/{invitation_id}/accept`
- `PATCH /api/teams/{team_id}/members/{member_id}/role`
- Extendimos `supabase/schema.sql` con `team_invitations`.
- Dejamos la logica de manager para crear equipos, invitar miembros, aceptar invitaciones y cambiar roles.

### Verificaciones hechas hoy

- `python -m compileall app`
- El backend levanta con todas las rutas nuevas cargadas.
- `GET /api/health` responde `{"status":"ok"}`
- `POST /api/auth/validate-email` responde correctamente para dominio publico y dominio propio.

### Pendiente para probar con Supabase real

- Confirmar que `register` y `login` funcionan con el proyecto real de Supabase y las llaves definitivas.
- Ejecutar la version nueva de `supabase/schema.sql`.
- Decidir si en Supabase Auth se deja apagada la confirmacion por correo para facilitar la demo.

## 2026-06-02

### Lo que hicimos hoy en Epica 2 backend

- Implementamos la base de `Gini Profile` en el backend.
- Extendimos `profiles` con `professional_role`, `profile_version` y `onboarding_completed_at`.
- Agregamos la tabla `profile_assessments` para guardar el historial de evaluaciones iniciales.
- Creamos un banco de preguntas por track para Azure, AWS y GitHub.
- Agregamos deteccion automatica de track a partir de la certificacion objetivo.
- Agregamos la ruta `GET /api/users/me/onboarding/questions`.
- Agregamos la ruta `POST /api/users/me/onboarding/evaluate`.
- Agregamos la ruta `GET /api/users/me/onboarding/latest`.
- Dejamos la evaluacion con score, deteccion de nivel `basic`, `intermediate` o `advanced`, resumen y recomendaciones.
- Dejamos sincronizacion del perfil base despues de la evaluacion inicial para que Gini Planner y Gini Path puedan usarla despues.

### Verificaciones hechas hoy

- `python -m compileall app`
- El backend carga las rutas nuevas de onboarding sin errores.
- `GET /api/users/me/onboarding/questions?target_certification=AZ-204` responde con preguntas de Azure.
- `GET /api/users/me/onboarding/questions?target_certification=GitHub Foundations` responde con preguntas de GitHub.

### Pendiente para validar con Supabase real

- Probar `POST /api/users/me/onboarding/evaluate` con un token real de Supabase.
- Ejecutar la nueva migracion de `supabase/schema.sql` para crear `profile_assessments` y los campos extra de `profiles`.

## 2026-06-02

### Lo que hicimos hoy en backend grande

- Extendimos el backend para cubrir de forma base todas las épicas del producto.
- Agregamos el catalogo de certificaciones y la generacion de rutas de aprendizaje.
- Agregamos la generacion de planes semanales con fecha de vencimiento y contexto mock de Work IQ.
- Agregamos asignacion de certificaciones a miembros del equipo.
- Agregamos sesiones de aprendizaje con recursos, pregunta obligatoria, dudas libres, evaluacion, encuesta e integridad mock.
- Agregamos recordatorios de `Gini Coach`.
- Agregamos dashboard de manager con progreso, riesgo y mensaje de apoyo.
- Agregamos examen final, envio de respuestas y certificados.
- Agregamos sugerencias de mejora con clasificacion `applicable`, `needs_context` y `queued`.
- Agregamos endpoint de estado tecnico para integraciones externas.
- Creamos documentacion por épica para que el agente de frontend pueda avanzar mas rapido.
- Creamos un markdown de requerimientos tecnicos externos para que sepas exactamente que completar en Supabase y Azure.
- Creamos `infra/validate_setup.py` para validar configuracion externa pendiente.

### Endpoints nuevos clave

- `GET /api/certifications`
- `POST /api/learning/routes`
- `GET /api/learning/routes/latest`
- `POST /api/learning/plans`
- `GET /api/learning/plans/latest`
- `POST /api/learning/teams/{team_id}/assignments`
- `POST /api/sessions`
- `GET /api/sessions/{session_id}`
- `POST /api/sessions/{session_id}/mandatory-answer`
- `POST /api/sessions/{session_id}/free-question`
- `POST /api/sessions/{session_id}/evaluation`
- `POST /api/sessions/{session_id}/survey`
- `POST /api/sessions/{session_id}/integrity-event`
- `POST /api/coach/reminders/generate`
- `GET /api/coach/reminders/mine`
- `GET /api/manager/teams/{team_id}/dashboard`
- `GET /api/manager/teams/{team_id}/members/{member_id}`
- `POST /api/manager/teams/{team_id}/members/{member_id}/support-message`
- `POST /api/exams/final`
- `POST /api/exams/final/{attempt_id}/submit`
- `GET /api/exams/certificates/mine`
- `POST /api/suggestions`
- `GET /api/suggestions/mine`
- `GET /api/suggestions/team/{team_id}/summary`
- `GET /api/system/integrations/status`

### Verificaciones hechas hoy

- `python -m compileall app`
- `python ..\infra\validate_setup.py`
- `GET /api/certifications`
- `GET /api/system/integrations/status`
- `GET /api/users/me/onboarding/questions?target_certification=AWS Cloud Practitioner`

### Pendientes reales para dejar todo funcional con servicios externos

- Ejecutar la version nueva de `supabase/schema.sql`.
- Completar `server/.env` con llaves reales de Supabase.
- Completar variables de Azure AI Foundry.
- Completar variables de Azure AI Search y Blob Storage.
- Completar variables de Work IQ o Microsoft Graph.
- Probar flujos autenticados completos con tokens reales.

### Archivos clave

- `server/.env.example`
- `server/app/main.py`
- `server/app/core/config.py`
- `server/app/core/security.py`
- `server/app/services/profile_service.py`
- `client/public/runtime-config.js`
- `client/src/app/core/auth/auth.store.ts`
- `client/src/app/core/services/api.service.ts`
- `client/src/app/features/auth/login-page/login-page.component.ts`
- `client/src/app/features/dashboard/dashboard-page.component.ts`
- `server/app/api/routes/auth.py`
- `server/app/api/routes/teams.py`
- `server/app/api/routes/users.py`
- `server/app/models/team.py`
- `server/app/models/onboarding.py`
- `server/app/models/certification.py`
- `server/app/models/learning.py`
- `server/app/models/session.py`
- `server/app/models/coach.py`
- `server/app/models/manager.py`
- `server/app/models/exam.py`
- `server/app/models/suggestion.py`
- `server/app/models/integration.py`
- `server/app/services/auth_service.py`
- `server/app/services/onboarding_catalog.py`
- `server/app/services/onboarding_service.py`
- `server/app/services/catalog_service.py`
- `server/app/services/learning_service.py`
- `server/app/services/session_service.py`
- `server/app/services/coach_service.py`
- `server/app/services/manager_service.py`
- `server/app/services/exam_service.py`
- `server/app/services/suggestion_service.py`
- `server/app/services/integration_service.py`
- `server/app/services/team_service.py`
- `Documentation/Backend_Epica_1.md`
- `Documentation/Backend_Epica_2.md`
- `Documentation/Backend_Epica_3.md`
- `Documentation/Backend_Epica_4.md`
- `Documentation/Backend_Epica_5.md`
- `Documentation/Backend_Epica_6.md`
- `Documentation/Backend_Epica_7.md`
- `Documentation/Backend_Epica_8.md`
- `Documentation/Backend_Epica_9.md`
- `Documentation/Backend_Technical_Requirements.md`
- `infra/validate_setup.py`
- `supabase/schema.sql`

### Verificaciones hechas

- `client` compila con `npm run build`
- `server` levanta con `uvicorn`
- `GET /api/health` responde `{"status":"ok"}`

### Configuracion pendiente para correr con datos reales

- Completar `server/.env` usando `server/.env.example`
- Completar `client/public/runtime-config.js` con `SUPABASE_URL`, `SUPABASE_ANON_KEY` y `apiBaseUrl`
- Ejecutar `supabase/schema.sql` en el proyecto real de Supabase
- Desactivar confirmacion por correo en Supabase Auth si queremos demo inmediata sin email

### Siguiente paso recomendado

- Completar configuracion externa real
- Luego conectar el frontend a todas las APIs ya disponibles

## 2026-06-02

### Lo que corregimos hoy en backend despues de la revision

- Endurecimos la Épica 2 para que onboarding exija entre 5 y 10 respuestas.
- La encuesta de sesion ahora puede saltarse con `skipped: true` y el sistema registra ese estado.
- La Épica 4 ahora bloquea avance real:
- no deja evaluar si no se aprobó la pregunta obligatoria
- quiz y lab devuelven `needs_retry` si no alcanzan el minimo
- la encuesta actualiza `learning_style` automaticamente cuando aplica
- los eventos de integridad ahora tambien generan notificacion para manager
- La Épica 3 y 5 ahora generan planes por miembro en asignaciones de equipo y crean una notificacion inicial de asignacion.
- El contexto mock de Work IQ ahora incluye dias recomendados, dias a evitar, ventanas preferidas y offsets de alerta.
- Gini Coach ya genera alertas de vencimiento a 7 dias, 3 dias y el dia del vencimiento cuando corresponde.
- La Épica 6 ahora calcula `top_gaps` desde errores reales recientes y agrega:
- `GET /api/manager/teams/{team_id}/weekly-summary`
- `GET /api/manager/teams/{team_id}/export-pdf`
- La Épica 7 ahora:
- exige secciones completadas antes del examen final
- genera entre 15 y 25 preguntas con limite de tiempo
- devuelve secciones falladas y recomendaciones de refuerzo
- recomienda la siguiente certificacion si el usuario aprueba
- genera certificado con nombre y PDF descargable en `/generated/certificates/...`
- Agregamos `infra/provision.sh` como base del provisioning tecnico para la hackathon.

### Verificaciones hechas hoy

- `python -m compileall app`
- Generacion de PDF sintetico validada con `server/generated/test-smoke.pdf`

### Bloqueadores o notas

- El import runtime completo de `app.main` en esta maquina fallo porque al entorno local le falta `email-validator` instalado, aunque ya esta declarado en `server/requirements.txt`.
- Para Supabase real hay que volver a ejecutar `supabase/schema.sql` porque agregamos columnas nuevas en `exam_attempts` y `certificates`.

## 2026-06-02

### Lo que hicimos hoy con Postman

- Reemplazamos la coleccion parcial de Épica 1 por una coleccion backend completa en `Documentation/RetAIM_Epica_1.postman_collection.json`.
- La coleccion ahora cubre:
- health y estado tecnico
- auth y equipos
- onboarding
- learning
- sessions
- coach
- manager
- exams
- suggestions
- Corregimos payloads viejos que ya no coincidian con los enums reales del backend.
- Agregamos variables y scripts para capturar automaticamente:
- tokens
- ids de usuario
- teamId
- invitationId
- routeId
- planId
- sectionId
- sessionId
- attemptId
- certificateId
- Dejamos notas dentro de la coleccion para endpoints con prerequisitos reales como examen final.

### Verificaciones hechas hoy

- `python -m json.tool Documentation/RetAIM_Epica_1.postman_collection.json`

## 2026-06-02

### Lo que hicimos hoy para plan de interfaz

- Creamos `Documentation/Frontend_Interface_Plan.md` como guia funcional para el frontend.
- Definimos:
- navegacion por rol
- flujo principal employee
- flujo principal manager
- pantallas recomendadas
- rutas sugeridas
- componentes compartidos
- orden recomendado de implementacion
- El documento aterriza el backend actual en una interfaz concreta para que el siguiente agente pueda construir sin adivinar.

## 2026-06-02

### Lo que hicimos hoy para direccion visual

- Creamos `Documentation/Stitch_UI_Prompt.md`.
- Dejamos un prompt maestro para generar todas las pantallas en Stitch.
- La direccion visual definida usa morado, azul, blanco y negro con varios degradados entre esos colores.
- El prompt ya incluye:
- estilo general
- tipografia
- componentes visuales
- estados
- responsividad
- lista completa de pantallas para employee y manager
- Tambien dejamos una version corta del prompt para pegar rapido si no quieres usar la version detallada.

## 2026-06-02

### Lo que implementamos hoy en frontend

- Reestructuramos `client` hacia una arquitectura por componentes y rutas privadas con `AppShell`.
- Agregamos navegacion por rol con sidebar, top level app shell y iconografia SVG profesional sin emojis.
- Cambiamos la direccion visual base del frontend a una paleta morado, azul, blanco y negro con degradados mas cercanos al prompt de Stitch.
- Expandimos `ApiService` para conectar el frontend con onboarding, learning, sessions, reminders, manager y certificados del backend.
- Agregamos guard para manager.
- Creamos vistas funcionales conectadas al backend para:
- dashboard principal
- onboarding
- plan de certificacion
- sesiones
- recordatorios
- certificados
- perfil
- dashboard manager
- equipo manager
- resumen semanal manager
- El frontend ya compila con estas rutas nuevas y deja una base lista para seguir refinando diseño y comportamiento.

### Verificaciones hechas hoy

- `npm run build`

### Bloqueadores o notas

- Intentamos leer proyectos de Stitch desde MCP pero la sesion actual respondio `Auth required`, asi que por ahora la implementacion visual se hizo siguiendo el plan de interfaz, el prompt visual y el backend real del repo.
- El build compila, pero Angular reporta que el bundle inicial supera el budget por el tamaño actual del MVP.

## 2026-06-02

### Lo que ajustamos hoy en frontend tomando `retaim-ui` como fuente real

- Dejamos de depender de Stitch y tomamos `retaim-ui` como referencia definitiva de diseño.
- Rehicimos `AppShell` para pasar de sidebar a `top nav` glassmorphism, mas alineado con las vistas HTML entregadas.
- Ajustamos el tema global a la direccion visual real de `retaim-ui` con `Plus Jakarta Sans`, `Inter`, halos atmosfericos y superficies morado azul sobre fondo oscuro.
- Adaptamos el dashboard principal employee al layout real con:
- hero de certificacion activa
- barra de progreso
- bloque de AI insight
- shelf de acciones rapidas
- Adaptamos el dashboard manager al layout real con:
- hero ejecutivo
- metricas superiores
- tabla de resumen de equipo
- panel lateral de assistant
- Creamos la vista Angular de `sugerencias` para reflejar `retaim-ui/sugerencias.html` y conectarla con `GET /api/suggestions/mine`.
- La navegacion ya incluye la nueva ruta `/suggestions`.
- Mantuvimos la conexion real al backend mientras aterrizamos el rediseño visual.

### Verificaciones hechas hoy

- `npm run build`

### Bloqueadores o notas

- El build ya no reporta advertencias de CSS por imports, pero el bundle inicial sigue por encima del budget actual de Angular.
- Aun faltan mas pantallas por alinear una a una con `retaim-ui`, pero la base visual ya quedo orientada al diseño correcto.

## 2026-06-05

### Modulo de cursos: implementacion por fases (F0-F6 + infra)

Reescribimos el modulo de cursos para pasar de plantillas hardcodeadas a contenido
real, tutor con agente y calificacion confiable. Todo degrada a mock si Foundry esta apagado.

- **F0 Modelo de datos**: nuevas tablas en `supabase/schema.sql` (`courses`,
  `course_sections`, `course_lessons`, `course_labs`, `lesson_completions`,
  `lesson_chat_messages`) con RLS. Modelos en `server/app/models/course.py`,
  servicio `course_service.py` (lectura + upsert idempotente) y ruta `/api/courses`.
- **F1 Ingesta**: `infra/ingest_content.py` baja la API publica de Microsoft Learn
  Catalog y genera cursos reales (Azure, GitHub) + plantilla sintetica para AWS.
  Escribe markdown en `synthetic-data/certifications/` (para indexar) y JSON por curso.
  Con `--push` sube a Supabase. Genera 4 cursos: AZ-900, AZ-204, GitHub Foundations, AWS CP.
- **F2 Foundry real**: `foundry_adapter.run_agent()` llama al modelo de Foundry con
  grounding en Azure AI Search, usando el system prompt de cada agente Gini desde sus
  JSON. La generacion de rutas ahora lee del catalogo real (lecciones, labs, duracion);
  `content_service.py` adapta el contenido al `learning_style`. Fallback total a mock.
- **F3 Tutor por leccion**: endpoints `POST/GET /api/sessions/{id}/lessons/{lesson_id}/chat`
  y `GET .../suggested-questions` con Gini Eval, persistidos en `lesson_chat_messages`.
  Reemplazamos la respuesta fija de `free-question` por una llamada real al agente.
- **F4 Calificacion real**: `assessment_service.py` genera quizzes/examen con Gini Eval
  o el banco real de `onboarding_catalog`, y califica labs por rubrica. El quiz se
  califica en el servidor contra la clave (ya no se confia en `is_correct` del cliente)
  y el examen ya no expone `correct_option_index` al cliente (`ExamQuestionPublic`).
- **F5 Certificado**: `pdf_service.generate_certificate_pdf` con diseño (apaisado,
  borde, branding) y endpoint publico `GET /api/exams/certificates/verify/{code}`.
- **F6 Orquestacion**: `orchestrator_service.py` (Gini Router) coordina al completar
  leccion: progreso -> Gini Insight -> Gini Coach (siguiente recordatorio) -> proximo
  paso. Endpoint `POST /api/sessions/{id}/lessons/{lesson_id}/complete`.
- **Infra**: `foundry.sh` ahora despliega el modelo `gpt-4o-mini` automaticamente;
  `provision.sh` corre la ingesta antes de indexar. Agregamos `openai` a
  `server/requirements.txt`, `azure_foundry_api_version` a config y creamos `server/.env.example`.

### Verificaciones hechas hoy

- `python -m compileall app` (todo el backend)
- `import app.main` OK: 52 rutas, incluidas las 6 nuevas de cursos/tutor/verify.
- `infra/ingest_content.py` corrido contra MS Learn real (4 cursos, archivos generados).
- Funciones de `assessment_service` probadas en modo fallback (quiz/examen/lab).
- `generate_certificate_pdf` produce un PDF valido.
- `bash -n` sobre `provision.sh` y `foundry.sh`.

### Pendientes para correr con servicios reales

- Ejecutar la nueva version de `supabase/schema.sql` (tablas de cursos).
- Correr `python infra/ingest_content.py --push` con `server/.env` configurado para
  poblar el catalogo en Supabase (o dejar que `provision.sh` lo haga).
- Completar variables de Foundry/Search en `server/.env` y `ENABLE_EXTERNAL_AI=true`
  para activar agentes reales; sin esto todo corre en modo mock funcional.
- La API de MS Learn requirio SSL relajado en una maquina (usar `--insecure-ssl` o
  `INGEST_INSECURE_SSL=1` solo si tu red rompe la cadena TLS).

### Ampliacion de cursos y costos (mismo dia)

- **Modo catalogo en `ingest_content.py`**: con `--catalog` ahora convierte CADA
  learning path de Microsoft Learn en un curso. Verificado: genera **299 cursos**
  (270 Azure, 28 GitHub, 1 AWS sintetico) con 1278 lecciones reales, 0 errores.
  Flags: `--products` (default azure,github), `--levels` (default beginner,intermediate),
  `--limit`. Los 4 cursos curados (AZ-900, AZ-204, etc.) siguen disponibles sin `--catalog`.
- **Costo de Azure AI Search**: `knowledge_base.sh` pasaba `--sku basic` (~$75/mes).
  Lo cambiamos a `AZURE_SEARCH_SKU` con default **free ($0)**, suficiente para el demo.
  Ademas `provision.sh` acepta `SKIP_SEARCH=true` para omitir Search por completo: el
  grounding del tutor/contenido ya funciona inyectando el contenido de la leccion en el
  prompt, asi que Azure AI Search es opcional (solo agrega busqueda amplia del KB).
- Nota: en Windows algunos paths de MS Learn superaban 260 chars; truncamos los nombres
  de archivo del markdown (el JSON/DB conserva las claves completas).
- **`/api/certifications` ahora sale de la tabla `courses`** (una sola query, con
  fallback al catalogo curado de 4 si la tabla esta vacia). Asi el frontend ve los 299
  cursos ingeridos. `catalog_service.list_certifications()` mapea cada curso a
  `CertificationSummary`. Verificado con `import app.main`.
- **Azure AI Search en Free**: confirmado dejar `AZURE_SEARCH_SKU=free` ($0) como
  default. El provisioning real lo corre el equipo con su cuenta de Azure (`provision.sh`).

### Frontend del modulo de cursos (mismo dia)

Conectamos el frontend Angular a los endpoints nuevos con una UI muy mejorada
(glassmorphism, gradientes, cards, carrusel, animaciones). Build limpio sin warnings.

- **Cimientos (A)**: `client/.../core/services/api.service.ts` con tipos y metodos para
  courses, tutor por leccion, completar leccion y verificar certificado. Corregido
  `submitEvaluation` para enviar `quiz_answers` (antes mandaba `is_correct` falso que el
  backend ya ignora).
- **Design system**: nuevas utilidades globales en `src/styles.css` (btn, chip, course-card,
  shelf/carrusel, drawer, skeleton, tutor bubbles, animaciones).
- **Catalogo (B)**: nueva pantalla `/catalog` (`features/catalog/`) con buscador, filtros por
  track y nivel, carrusel de destacados, grid de cards y drawer de detalle con temario
  (secciones -> lecciones -> labs) y CTA "generar ruta y plan". Link "Cursos" en el nav.
- **Home (B2)**: el dashboard ahora trae un carrusel "Explorar cursos" con cards.
- **Sesion + tutor (C)**: `features/learning/learning-session-page` reescrita: navegacion
  por lecciones, contenido + fuentes citadas, **panel del tutor IA flotante** (chat por
  leccion + chips de preguntas sugeridas), **quiz real** (render de `quiz_questions`,
  envia `quiz_answers`, maneja needs_retry), pregunta obligatoria, encuesta, y boton
  "Completar leccion" que muestra progreso + mensaje de coach + proximo paso (orquestacion).
- **Examen (D)**: nueva ruta `/exam` (`features/exam/`) full-focus con cronometro, una
  pregunta por vista, y pantalla de resultado aprobado/no aprobado con secciones a reforzar
  y siguiente certificacion.
- **Pulido (E)**: subimos budgets en `angular.json`, build sin warnings.

### Verificaciones hechas hoy (frontend)

- `npx ng build` limpio (corrido dentro de WSL con node nvm; el npm de Windows sobre el
  share UNC crasheaba con "Exit handler never called").

### Notas / pendientes frontend

- El entorno: las deps del frontend se instalan dentro de WSL (`/home/damon/.nvm/.../npm`),
  NO con el npm de Windows sobre `\\wsl.localhost` (ese crashea).
- El tutor y el quiz real lucen mejor con Foundry activo, pero funcionan en modo mock.
- Pendiente opcional: UI de verificacion publica de certificado, y progreso real del
  dashboard desde `lesson_completions` (hoy es estimado).

### RAG con Supabase pgvector (reemplaza Azure AI Search) — mismo dia

Decision: en vez de Azure AI Search (caro / free no integrable), usamos Supabase pgvector
como base vectorial para RAG. El tutor recupera fragmentos REALES del contenido completo
de las lecciones y los pasa como contexto a GPT-4o con prompt estricto (no inventar).
Eliminamos el enfoque anterior de inyectar el resumen de la leccion en cada consulta.

- **Schema** (`supabase/schema.sql`): `create extension vector`; tabla `lesson_chunks`
  (certification_code, lesson_key, content, embedding vector(1024)); indice HNSW cosine;
  funcion `match_lesson_chunks(query_embedding, match_count, filter_certification)`.
- **Embeddings**: `server/app/services/embedding_service.py` con **fastembed + BGE-M3**
  (1024 dim, multilingue, gratis; alternativa multilingual-e5-large). `fastembed==0.4.2`
  en requirements. Config `embedding_model`/`embedding_dim` en core/config.
- **RAG**: `server/app/services/rag_service.py` (`upsert_lesson_chunks`, `retrieve`).
- **Tutor reescrito** (`lesson_tutor_service.py`): retrieve -> contexto -> GPT-4o con prompt
  estricto; con Foundry genera, sin Foundry responde extractivo (top chunk), sin chunks
  da mensaje honesto. `answer_free_question` (session_service) tambien pasa por RAG.
  Borramos `content_service.py` (era el inject de adaptacion, codigo muerto).
- **Ingesta** (`infra/ingest_content.py`): flag `--rag` baja el TEXTO COMPLETO de las
  unidades de MS Learn (patron de URL verificado: `<module>/<n>-<ultimo-segmento-uid>`),
  lo limpia, trocea (~1800 chars, overlap 200), embebe y sube a pgvector. Default de
  cursos bajado a **50** (`--limit 50`).

Comando para poblar RAG: `python infra/ingest_content.py --catalog --rag --push`
(la primera vez descarga el modelo BGE-M3 ~2GB; tarda varios minutos por la descarga de
unidades + embeddings).

Verificado: `compileall` + `import app.main` OK; AST de ingest OK; extraccion de texto de
unidades probada en vivo. PENDIENTE de correr con Supabase real: ejecutar el nuevo
`schema.sql` (incluye pgvector), `pip install -r requirements.txt` (fastembed), y la
ingesta `--rag`.
