# Backend Epica 9

## Objetivo

Recepcion y clasificacion de sugerencias de mejora con logica tipo `Gini Insight`.

## Endpoints

- `POST /api/suggestions`
- `GET /api/suggestions/mine`
- `GET /api/suggestions/team/{team_id}/summary`

## Notas para frontend

- `POST /suggestions` devuelve el estado evaluado:
- `applicable`
- `needs_context`
- `queued`
- `mine` lista las sugerencias del usuario autenticado.
- `team/{team_id}/summary` es para manager y devuelve totales por categoria y por estado.
- La UI del manager debe ser agregada y no exponer sugerencias individuales atribuidas a una persona.

## Entidades principales

- `suggestions`
