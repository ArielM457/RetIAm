# Backend Epica 3

## Objetivo

Generar rutas y planes de certificacion a partir del perfil ya evaluado.

## Endpoints

- `GET /api/certifications`
- `POST /api/learning/routes`
- `GET /api/learning/routes/latest`
- `POST /api/learning/plans`
- `GET /api/learning/plans/latest`
- `POST /api/learning/teams/{team_id}/assignments`

## Notas para frontend

- `certifications` sirve para poblar el catalogo inicial.
- `routes` genera una ruta con secciones y recursos.
- `plans` toma una ruta generada y devuelve hitos semanales, fecha de vencimiento y contexto mock de Work IQ con:
- `recommended_study_days`
- `avoid_days`
- `preferred_delivery_windows`
- `deadline_alert_offsets_days`
- El frontend debe mostrar siempre el `deadline_at` del plan.
- Un manager puede asignar una certificacion a varios miembros de su equipo con `assignments`.
- Esa asignacion ya dispara la generacion del route y del plan por cada miembro y crea una notificacion inicial.

## Entidades principales

- `learning_routes`
- `study_plans`
- `team_certification_assignments`
