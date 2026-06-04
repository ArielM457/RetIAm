# Backend Epica 7

## Objetivo

Examen final y generacion de certificados RetAIM.

## Endpoints

- `POST /api/exams/final`
- `POST /api/exams/final/{attempt_id}/submit`
- `GET /api/exams/certificates/mine`

## Notas para frontend

- `final` crea un intento de examen a partir de un `plan_id`.
- Solo deja iniciar el examen si todas las secciones del plan ya estan completadas.
- El examen trae entre 15 y 25 preguntas y devuelve `time_limit_minutes`.
- `submit` recibe las respuestas elegidas y devuelve score, max score, estado `passed`, `failed_sections`, `recommendations` y `next_certification`.
- Si aprueba, el backend crea automaticamente un certificado en `certificates` con nombre, score, codigo verificable y `pdf_url`.
- Si no aprueba, el plan pasa a `needs_reinforcement`.
- `certificates/mine` lista todos los certificados del usuario.

## Entidades principales

- `exam_attempts`
- `certificates`
