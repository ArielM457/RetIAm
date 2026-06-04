# Backend Epica 4

## Objetivo

Sesiones de aprendizaje, preguntas obligatorias, dudas libres, evaluaciones, encuesta final e integridad mock.

## Endpoints

- `POST /api/sessions`
- `GET /api/sessions/{session_id}`
- `POST /api/sessions/{session_id}/mandatory-answer`
- `POST /api/sessions/{session_id}/free-question`
- `POST /api/sessions/{session_id}/evaluation`
- `POST /api/sessions/{session_id}/survey`
- `POST /api/sessions/{session_id}/integrity-event`

## Notas para frontend

- Cada sesion se crea con `plan_id`, `section_id`, `section_title` y `session_type`.
- La respuesta inicial ya trae:
- recursos
- pregunta obligatoria
- estado
- Para teoria o quiz, usar `mandatory-answer` y luego `evaluation`.
- `evaluation` ahora bloquea el avance si la pregunta obligatoria no fue respondida correctamente.
- Si quiz o lab no llegan al minimo de aprobacion, la sesion vuelve con estado `needs_retry`.
- Para labs, mandar `lab_solution_summary` a `evaluation`.
- `survey` acepta `skipped: true` para que la encuesta sea saltable.
- Si la encuesta no se salta, el backend usa `preferred_format` para ajustar automaticamente `learning_style`.
- `integrity-event` sirve para el mock de cambio de pestaña o eventos de supervision y ademas genera notificacion para manager.

## Entidades principales

- `learning_sessions`
- `integrity_events`
