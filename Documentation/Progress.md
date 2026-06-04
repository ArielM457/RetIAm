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
