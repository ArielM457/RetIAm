# Frontend Interface Plan

## Objetivo

Definir como deberia verse y fluir la interfaz de RetAIM para que el agente que construya el frontend tenga una guia clara de pantallas, pestañas, estados y prioridades.

Este plan toma como fuente de verdad:

- `README.md`
- `Documentation/USER_STORIES.md`
- documentacion backend por epica
- rutas reales ya disponibles en `server/app/api/routes`

## Principios de UX

- La plataforma debe sentirse simple aunque por dentro tenga muchos agentes.
- El usuario no deberia pensar en agentes tecnicos. Debe entender tareas concretas como aprender, avanzar, ver riesgo o ayudar a su equipo.
- Cada pantalla debe responder una pregunta clara:
- employee: que hago hoy, que me falta, como avanzo
- manager: quien necesita ayuda, que riesgo tiene el equipo, que brechas tenemos
- El flujo principal debe ser corto:
- entrar
- completar perfil
- elegir certificacion
- recibir plan
- estudiar
- rendir examen
- ver resultado

## Roles

## Employee

Necesita:

- login y registro
- onboarding inicial
- dashboard personal
- plan de certificacion
- sesiones de aprendizaje
- recordatorios
- examen final y certificado
- sugerencias
- perfil editable

## Manager

Necesita todo lo anterior a nivel basico de cuenta, pero sobre todo:

- crear y administrar equipo
- invitar miembros
- ver dashboard del equipo
- ver riesgos
- ver brechas
- ver resumen semanal
- exportar PDF
- enviar mensajes de apoyo

## Arquitectura de navegacion recomendada

## Navegacion publica

- `/login`
- `/register` si se separa visualmente del login

## Navegacion privada employee

Sidebar o tab bar principal:

1. `Inicio`
2. `Mi Plan`
3. `Sesiones`
4. `Recordatorios`
5. `Certificados`
6. `Perfil`

Acciones globales:

- `Dejar sugerencia`
- `Cerrar sesion`

## Navegacion privada manager

Sidebar o tab bar principal:

1. `Inicio`
2. `Equipo`
3. `Miembros`
4. `Brechas`
5. `Resumen semanal`
6. `Perfil`

Acciones globales:

- `Crear equipo`
- `Invitar miembros`
- `Exportar PDF`
- `Cerrar sesion`

## Flujo general del producto

## Flujo employee

1. Login o registro
2. Validacion de perfil base
3. Si no completó onboarding:
- ir a onboarding
4. Si ya completó onboarding pero no tiene ruta:
- ir a seleccion de certificacion
5. Si ya tiene ruta y plan:
- entrar a dashboard personal
6. Desde dashboard:
- abrir sesion pendiente
- revisar hitos
- ver deadline
- generar recordatorios
7. Al completar secciones:
- habilitar examen final
8. Si aprueba:
- mostrar certificado
- sugerir siguiente certificacion
9. Si no aprueba:
- mostrar secciones a reforzar
- volver a plan y sesiones

## Flujo manager

1. Login o registro
2. Crear equipo si no existe
3. Invitar miembros
4. Ver dashboard general del equipo
5. Entrar al detalle de miembros en riesgo
6. Asignar certificacion al equipo o a miembros concretos
7. Revisar brechas agregadas
8. Consultar resumen semanal
9. Exportar PDF

## Pantallas recomendadas

## 1. Login y registro

Ruta:

- `/login`

Objetivo:

- autenticar con Supabase
- registrar cuenta nueva
- elegir rol inicial manager o employee

Componentes:

- hero corto con propuesta de valor
- tabs `Iniciar sesion` y `Crear cuenta`
- formulario con email, password, full name y role en registro
- mensaje de recomendacion si el dominio es publico

Endpoints:

- `POST /api/auth/validate-email`
- `POST /api/auth/register`
- `POST /api/auth/login`

## 2. Onboarding inicial

Ruta:

- `/onboarding`

Objetivo:

- capturar rol profesional, certificacion objetivo, horas por semana, horario preferido y estilo de aprendizaje
- responder 5 a 10 preguntas

Subpasos:

1. Datos base
2. Preferencias de estudio
3. Preguntas tecnicas
4. Resultado del perfil

Componentes:

- progress stepper
- formulario inicial
- tarjeta de pregunta con opciones
- resumen final con nivel detectado

Endpoints:

- `GET /api/users/me/onboarding/questions`
- `POST /api/users/me/onboarding/evaluate`
- `GET /api/users/me/onboarding/latest`

## 3. Dashboard personal

Ruta:

- `/dashboard`

Objetivo:

- decirle al usuario que hacer hoy

Bloques:

- certificacion actual
- nivel detectado
- progreso general
- deadline
- siguiente hito semanal
- CTA `Continuar sesion`
- CTA `Generar recordatorios`
- estado de examen final
- ultima sugerencia o tip del sistema

Datos que deberia consolidar el frontend:

- `GET /api/users/me`
- `GET /api/learning/routes/latest`
- `GET /api/learning/plans/latest`
- `GET /api/coach/reminders/mine`
- `GET /api/exams/certificates/mine`

## 4. Seleccion de certificacion y plan

Ruta:

- `/plan/new`

Objetivo:

- elegir certificacion
- generar ruta
- generar plan

Flujo:

1. listar certificaciones
2. elegir una
3. generar ruta
4. mostrar secciones
5. confirmar plan
6. generar plan

Pantalla recomendada:

- columna izquierda con catalogo
- columna derecha con preview de ruta y horas estimadas

Endpoints:

- `GET /api/certifications`
- `POST /api/learning/routes`
- `POST /api/learning/plans`

## 5. Mi plan

Ruta:

- `/plan`

Objetivo:

- mostrar la ruta ya generada y sus hitos semanales

Bloques:

- header con certificacion, deadline y estado
- timeline de hitos por semana
- lista de secciones
- indicador de dias recomendados y ventanas sugeridas por Work IQ mock
- CTA `Iniciar sesion`

Endpoint principal:

- `GET /api/learning/plans/latest`

## 6. Sesion de aprendizaje

Ruta:

- `/sessions/:sessionId`

Objetivo:

- resolver una sesion completa de estudio

Estructura recomendada:

- encabezado con seccion, tipo y estado
- panel de recursos
- bloque de pregunta obligatoria
- bloque de preguntas libres
- bloque de evaluacion
- bloque de encuesta final

Comportamiento clave:

- no mostrar boton de continuar si la pregunta obligatoria no fue aprobada
- si la evaluacion falla, mostrar `needs_retry` y CTA `Repasar y reintentar`
- si la encuesta se salta, registrar ese evento sin bloquear salida

Endpoints:

- `POST /api/sessions`
- `GET /api/sessions/{session_id}`
- `POST /api/sessions/{session_id}/mandatory-answer`
- `POST /api/sessions/{session_id}/free-question`
- `POST /api/sessions/{session_id}/evaluation`
- `POST /api/sessions/{session_id}/survey`
- `POST /api/sessions/{session_id}/integrity-event`

## 7. Recordatorios

Ruta:

- `/reminders`

Objetivo:

- mostrar recordatorios generados y el contexto recomendado de estudio

Bloques:

- CTA `Generar recordatorios`
- lista cronologica de recordatorios
- resumen del tono actual
- dias de alerta de vencimiento
- horarios preferidos sugeridos

Endpoints:

- `POST /api/coach/reminders/generate`
- `GET /api/coach/reminders/mine`

## 8. Examen final

Ruta:

- `/exam/final`

Objetivo:

- rendir el examen solo si ya completó todas las secciones

Estructura:

- aviso de prerequisito
- cronometro visible
- contador de preguntas
- una pregunta por vista o bloques cortos
- confirmacion antes de enviar

Estados:

- no habilitado
- en curso
- aprobado
- no aprobado con refuerzo

Endpoints:

- `POST /api/exams/final`
- `POST /api/exams/final/{attempt_id}/submit`

## 9. Resultado y certificado

Ruta:

- `/certificates`
- `/certificates/:certificateId`

Objetivo:

- mostrar score, estado, recomendaciones o certificado

Si aprueba:

- mostrar badge de logro
- link a PDF
- siguiente certificacion sugerida

Si no aprueba:

- mostrar secciones falladas
- recomendaciones
- CTA `Volver al plan`

Endpoint:

- `GET /api/exams/certificates/mine`

## 10. Perfil

Ruta:

- `/profile`

Objetivo:

- ver y editar perfil base

Campos:

- full name
- professional role
- target certification
- weekly hours
- preferred time
- learning style

Endpoints:

- `GET /api/users/me`
- `PATCH /api/users/me`
- `GET /api/users/me/onboarding/latest`

## 11. Sugerencias

Patron recomendado:

- modal global o drawer accesible desde cualquier pantalla privada

Ruta alternativa si quieren pagina dedicada:

- `/suggestions`

Objetivo:

- enviar sugerencias sin romper el flujo principal

Employee:

- crear sugerencia
- ver mis sugerencias

Manager:

- ver resumen agregado del equipo

Endpoints:

- `POST /api/suggestions`
- `GET /api/suggestions/mine`
- `GET /api/suggestions/team/{team_id}/summary`

## 12. Dashboard manager

Ruta:

- `/manager/dashboard`

Objetivo:

- mostrar estado general del equipo en una sola vista

Bloques:

- progreso promedio del equipo
- miembros por riesgo
- top 3 brechas
- CTA a detalle de miembro
- CTA a resumen semanal
- CTA a exportar PDF

Endpoint:

- `GET /api/manager/teams/{team_id}/dashboard`

## 13. Equipo y miembros

Rutas:

- `/manager/team`
- `/manager/team/members/:memberId`

Objetivo:

- administrar equipo e intervenir sobre miembros

Pantalla equipo:

- datos del equipo
- miembros
- invitaciones pendientes
- formulario de invitacion
- accion para asignar certificacion

Pantalla miembro:

- certificacion actual
- progreso
- riesgo
- dias a deadline
- secciones pendientes
- mensaje de apoyo

Endpoints:

- `GET /api/teams`
- `POST /api/teams`
- `GET /api/teams/{team_id}/members`
- `POST /api/teams/{team_id}/invites`
- `GET /api/teams/invitations/mine`
- `POST /api/teams/invitations/{invitation_id}/accept`
- `PATCH /api/teams/{team_id}/members/{member_id}/role`
- `POST /api/learning/teams/{team_id}/assignments`
- `GET /api/manager/teams/{team_id}/members/{member_id}`
- `POST /api/manager/teams/{team_id}/members/{member_id}/support-message`

## 14. Brechas, resumen semanal y export

Rutas:

- `/manager/gaps`
- `/manager/weekly-summary`

Objetivo:

- separar la capa analitica del dashboard principal si quieren una experiencia mas clara

Pantalla brechas:

- top gaps
- explicacion de por que esos temas estan arriba
- sugerencia de accion grupal

Pantalla resumen semanal:

- highlights
- riesgos
- proximos vencimientos
- boton `Exportar PDF`

Endpoints:

- `GET /api/manager/teams/{team_id}/weekly-summary`
- `GET /api/manager/teams/{team_id}/export-pdf`

## Mapa de rutas recomendado

```text
/login
/onboarding
/dashboard
/plan/new
/plan
/sessions/:sessionId
/reminders
/exam/final
/certificates
/profile
/manager/dashboard
/manager/team
/manager/team/members/:memberId
/manager/gaps
/manager/weekly-summary
```

## Componentes compartidos recomendados

- `AppShell`
- `Sidebar`
- `Topbar`
- `RoleBadge`
- `ProgressCard`
- `DeadlineCard`
- `SectionTimeline`
- `ResourceList`
- `QuestionCard`
- `ReminderList`
- `RiskPill`
- `CertificateCard`
- `SuggestionModal`
- `EmptyState`
- `ProtectedRoleGuard`

## Orden recomendado de implementacion

## Fase 1

- login
- app shell
- dashboard personal basico
- onboarding

## Fase 2

- catalogo y plan
- sesiones
- recordatorios

## Fase 3

- manager dashboard
- equipo y miembros
- sugerencias

## Fase 4

- examen final
- certificados
- resumen semanal
- export PDF

## Decisiones de UX importantes

- La primera pantalla privada no siempre debe ser el dashboard. Si el usuario no tiene onboarding completo, redirigir a onboarding.
- Si el usuario tiene onboarding pero no tiene plan, redirigir a seleccion de certificacion.
- El examen final no debe verse como disponible hasta que el frontend detecte progreso completo del plan.
- La sugerencia debe ser global porque una historia pide que sea accesible desde cualquier sesion.
- Manager y employee pueden compartir shell y componentes, pero no la misma pagina principal.

## Riesgos a cuidar en frontend

- No asumir que un usuario siempre tiene `team_id`.
- No asumir que el manager ya tiene equipo creado.
- No asumir que siempre existe una ruta o un plan.
- No asumir que el examen final puede empezar en cualquier momento.
- No exponer detalles de evaluaciones individuales en vistas de manager.

## Recomendacion final

Para la demo de hackathon conviene construir primero una experiencia muy solida para estos 3 recorridos:

1. employee entra, completa onboarding, genera plan y realiza una sesion
2. manager crea equipo, asigna certificacion y revisa dashboard
3. employee termina recorrido, rinde examen y ve certificado o refuerzo

Si esos 3 flujos se sienten bien, el resto de pantallas pueden crecer alrededor sin romper la narrativa principal del producto.
