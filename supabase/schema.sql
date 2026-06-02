create extension if not exists pgcrypto;

create table if not exists public.organizations (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    created_at timestamptz not null default timezone('utc', now())
);

create table if not exists public.profiles (
    id uuid primary key references auth.users (id) on delete cascade,
    email text not null unique,
    full_name text,
    role text not null default 'employee' check (role in ('manager', 'employee')),
    org_id uuid references public.organizations (id) on delete set null,
    team_id uuid,
    target_certification text,
    detected_level text check (detected_level in ('basic', 'intermediate', 'advanced')),
    weekly_hours_available integer,
    preferred_time text check (preferred_time in ('morning', 'afternoon', 'night')),
    learning_style text[] not null default '{}',
    created_at timestamptz not null default timezone('utc', now()),
    updated_at timestamptz not null default timezone('utc', now())
);

create table if not exists public.teams (
    id uuid primary key default gen_random_uuid(),
    org_id uuid not null references public.organizations (id) on delete cascade,
    name text not null,
    manager_id uuid not null references public.profiles (id) on delete restrict,
    created_at timestamptz not null default timezone('utc', now())
);

alter table public.profiles
    add constraint profiles_team_id_fkey
    foreign key (team_id) references public.teams (id) on delete set null;

create table if not exists public.team_members (
    team_id uuid not null references public.teams (id) on delete cascade,
    user_id uuid not null references public.profiles (id) on delete cascade,
    joined_at timestamptz not null default timezone('utc', now()),
    primary key (team_id, user_id)
);

create or replace function public.handle_profile_timestamp()
returns trigger
language plpgsql
as $$
begin
    new.updated_at = timezone('utc', now());
    return new;
end;
$$;

drop trigger if exists profiles_set_updated_at on public.profiles;
create trigger profiles_set_updated_at
before update on public.profiles
for each row
execute procedure public.handle_profile_timestamp();

alter table public.organizations enable row level security;
alter table public.profiles enable row level security;
alter table public.teams enable row level security;
alter table public.team_members enable row level security;

create policy "Users can read own profile"
on public.profiles
for select
to authenticated
using (auth.uid() = id);

create policy "Users can update own profile"
on public.profiles
for update
to authenticated
using (auth.uid() = id);

create policy "Users can insert own profile"
on public.profiles
for insert
to authenticated
with check (auth.uid() = id);
