-- =====================================================================
-- Migración incremental para el flujo Team Lead (curso personalizado,
-- ranking, notificaciones) + arreglo de columnas de teams.
--
-- SEGURA y RE-EJECUTABLE: solo usa "add column if not exists",
-- "drop constraint if exists" + add, y "create index if not exists".
-- NO crea tablas ni políticas, así que NO choca con "already exists".
--
-- Cómo usar: Supabase → SQL Editor → New query → pega ESTO → Run.
-- =====================================================================

-- 1) Equipos: columnas que usa la app al crear el equipo.
alter table public.teams add column if not exists sector text;
alter table public.teams add column if not exists member_capacity integer;
alter table public.teams add column if not exists work_style text;
alter table public.teams add column if not exists notes text;

-- 2) Cursos personalizados del team lead: scoping + certificación de plataforma.
alter table public.courses add column if not exists team_id uuid references public.teams (id) on delete cascade;
alter table public.courses add column if not exists created_by uuid references public.profiles (id) on delete set null;
alter table public.courses add column if not exists visibility text not null default 'global';
alter table public.courses add column if not exists is_certifiable boolean not null default false;

alter table public.courses drop constraint if exists courses_track_check;
alter table public.courses add constraint courses_track_check
    check (track in ('azure', 'aws', 'github', 'custom'));

alter table public.courses drop constraint if exists courses_source_check;
alter table public.courses add constraint courses_source_check
    check (source in ('template', 'ms_learn', 'synthetic', 'custom'));

alter table public.courses drop constraint if exists courses_visibility_check;
alter table public.courses add constraint courses_visibility_check
    check (visibility in ('global', 'team', 'org'));

create index if not exists courses_team_idx on public.courses (team_id);

-- 3) Notificaciones del manager (support directo + nudge generado por IA).
alter table public.coach_reminders drop constraint if exists coach_reminders_kind_check;
alter table public.coach_reminders add constraint coach_reminders_kind_check
    check (kind in ('standard', 'deadline', 'minimal', 'manager_support', 'nudge'));

-- 4) Refrescar el cache de esquema de PostgREST (para que la API vea los cambios).
NOTIFY pgrst, 'reload schema';
