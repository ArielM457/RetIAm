# Backend Epica 1

## Objetivo

Autenticacion mock con Supabase y gestion de equipos para manager y employee.

## Endpoints

- `POST /api/auth/validate-email`
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/users/me`
- `PATCH /api/users/me`
- `GET /api/teams`
- `POST /api/teams`
- `GET /api/teams/{team_id}/members`
- `POST /api/teams/{team_id}/invites`
- `GET /api/teams/invitations/mine`
- `POST /api/teams/invitations/{invitation_id}/accept`
- `PATCH /api/teams/{team_id}/members/{member_id}/role`

## Notas para frontend

- `validate-email` no bloquea dominios publicos. Solo recomienda usar uno institucional o del equipo.
- `register` y `login` devuelven tokens de Supabase y un resumen del usuario autenticado.
- Todas las rutas protegidas esperan `Authorization: Bearer <access_token>`.
- El manager puede crear varios equipos.
- Un employee solo puede pertenecer a un equipo a la vez.

## Entidades principales

- `profiles`
- `organizations`
- `teams`
- `team_members`
- `team_invitations`
