# Backend Epica 2

## Objetivo

Onboarding de `Gini Profile` para detectar nivel inicial, disponibilidad y estilo de aprendizaje.

## Endpoints

- `GET /api/users/me/onboarding/questions?target_certification=...`
- `POST /api/users/me/onboarding/evaluate`
- `GET /api/users/me/onboarding/latest`

## Notas para frontend

- Primero se consulta `questions` con la certificacion objetivo.
- El backend espera entre 5 y 10 respuestas en `answers`.
- Luego se manda a `evaluate`:
- `professional_role`
- `target_certification`
- `weekly_hours_available`
- `preferred_time`
- `learning_style`
- `answers`
- `evaluate` actualiza el perfil base del usuario y guarda el historial en `profile_assessments`.
- El estilo base del onboarding no queda congelado. Luego puede cambiar automaticamente segun encuestas y comportamiento de sesiones.
- El frontend puede usar `latest` para rehidratar el estado del onboarding si el usuario vuelve despues.

## Entidades principales

- `profiles`
- `profile_assessments`
