# Backend Epica 6

## Objetivo

Dashboard del manager con progreso agregado, riesgo y detalle de miembros.

## Endpoints

- `GET /api/manager/teams/{team_id}/dashboard`
- `GET /api/manager/teams/{team_id}/weekly-summary`
- `GET /api/manager/teams/{team_id}/export-pdf`
- `GET /api/manager/teams/{team_id}/members/{member_id}`
- `POST /api/manager/teams/{team_id}/members/{member_id}/support-message`

## Notas para frontend

- `dashboard` entrega el estado general del equipo y una lista resumida de miembros.
- `dashboard.top_gaps` ya no es fijo. Sale de errores recientes en sesiones y examenes del equipo.
- `weekly-summary` resume avances de la ultima semana, riesgos y proximos vencimientos para el panel de manager o un envio tipo Teams.
- `export-pdf` genera un PDF descargable con el resumen del equipo.
- `members/{member_id}` entrega el detalle individual permitido para manager.
- `support-message` es el punto para el CTA de enviar apoyo al miembro en riesgo.
- La UI no debe mostrar notas exactas de quizzes o labs porque el backend tampoco las expone al manager.

## Entidades principales

- `teams`
- `team_members`
- `study_plans`
- `learning_sessions`
