# Backend Epica 5

## Objetivo

Recordatorios adaptativos de `Gini Coach`.

## Endpoints

- `POST /api/coach/reminders/generate`
- `GET /api/coach/reminders/mine`

## Notas para frontend

- `generate` crea recordatorios derivados del plan actual y del contexto mock de Work IQ.
- El backend ya evita dias marcados como pesados en calendario mock y usa ventanas preferidas de entrega.
- Las alertas de vencimiento se generan para 7 dias, 3 dias y el dia de vencimiento si aplica.
- El tono puede variar entre `formal`, `concise` y `casual` segun la reaccion previa a recordatorios.
- `mine` lista los recordatorios ya programados para el usuario.
- Cada recordatorio tiene:
- `kind`
- `tone`
- `delivery_channel`
- `message`
- `scheduled_for`
- `status`

## Entidades principales

- `coach_reminders`
