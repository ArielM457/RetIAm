create extension if not exists pgcrypto;

alter table if exists public.teams
    add column if not exists sector text,
    add column if not exists member_capacity integer,
    add column if not exists work_style text,
    add column if not exists notes text;

create table if not exists public.team_access_codes (
    id uuid primary key default gen_random_uuid(),
    team_id uuid not null references public.teams (id) on delete cascade,
    org_id uuid not null references public.organizations (id) on delete cascade,
    code text not null unique,
    role text not null default 'employee' check (role in ('manager', 'employee')),
    status text not null default 'active' check (status in ('active', 'used', 'expired', 'cancelled')),
    created_by uuid not null references public.profiles (id) on delete cascade,
    used_by uuid references public.profiles (id) on delete set null,
    expires_at timestamptz not null,
    created_at timestamptz not null default timezone('utc', now()),
    used_at timestamptz
);

create index if not exists team_access_codes_active_team_idx
on public.team_access_codes (team_id, status);

alter table if exists public.team_access_codes enable row level security;
