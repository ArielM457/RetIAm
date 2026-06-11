-- Refactor incremental posterior al refactor base ya aplicado.
-- Este archivo solo agrega lo nuevo para el flujo de inscripcion y agenda.
-- Ejecutar en Supabase SQL Editor cuando la base ya tenga el refactor anterior.

create table if not exists public.course_enrollments (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.profiles (id) on delete cascade,
    course_id uuid not null references public.courses (id) on delete cascade,
    certification_code text not null,
    status text not null default 'enrolled' check (status in ('enrolled', 'active', 'paused', 'completed', 'cancelled')),
    enrolled_at timestamptz not null default timezone('utc', now()),
    activated_route_id uuid references public.learning_routes (id) on delete set null,
    activated_plan_id uuid references public.study_plans (id) on delete set null,
    preferences_snapshot jsonb not null default '{}'::jsonb,
    personalization_summary jsonb not null default '[]'::jsonb,
    current_section_id text,
    current_session_id text,
    unique (user_id, certification_code)
);

create index if not exists course_enrollments_user_status_idx
on public.course_enrollments (user_id, status, enrolled_at desc);

create table if not exists public.learning_agenda_items (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.profiles (id) on delete cascade,
    enrollment_id uuid references public.course_enrollments (id) on delete cascade,
    plan_id uuid references public.study_plans (id) on delete cascade,
    route_id uuid references public.learning_routes (id) on delete cascade,
    title text not null,
    item_type text not null check (item_type in ('study_session', 'review', 'lab', 'checkin', 'reminder')),
    related_session_id text,
    related_section_id text,
    related_lesson_ids jsonb not null default '[]'::jsonb,
    scheduled_start timestamptz not null,
    scheduled_end timestamptz not null,
    time_window text,
    status text not null default 'scheduled' check (status in ('scheduled', 'completed', 'missed', 'rescheduled', 'cancelled')),
    agenda_date date generated always as ((scheduled_start at time zone 'utc')::date) stored,
    metadata jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default timezone('utc', now()),
    updated_at timestamptz not null default timezone('utc', now())
);

create index if not exists learning_agenda_items_user_date_idx
on public.learning_agenda_items (user_id, agenda_date, scheduled_start);

create index if not exists learning_agenda_items_plan_idx
on public.learning_agenda_items (plan_id, status);

alter table if exists public.course_enrollments enable row level security;
alter table if exists public.learning_agenda_items enable row level security;

do $$
begin
    if not exists (
        select 1 from pg_policies
        where schemaname = 'public' and tablename = 'course_enrollments' and policyname = 'Users can read own enrollments'
    ) then
        create policy "Users can read own enrollments"
        on public.course_enrollments for select to authenticated using (auth.uid() = user_id);
    end if;

    if not exists (
        select 1 from pg_policies
        where schemaname = 'public' and tablename = 'course_enrollments' and policyname = 'Users can insert own enrollments'
    ) then
        create policy "Users can insert own enrollments"
        on public.course_enrollments for insert to authenticated with check (auth.uid() = user_id);
    end if;

    if not exists (
        select 1 from pg_policies
        where schemaname = 'public' and tablename = 'course_enrollments' and policyname = 'Users can update own enrollments'
    ) then
        create policy "Users can update own enrollments"
        on public.course_enrollments for update to authenticated using (auth.uid() = user_id);
    end if;

    if not exists (
        select 1 from pg_policies
        where schemaname = 'public' and tablename = 'learning_agenda_items' and policyname = 'Users can read own agenda items'
    ) then
        create policy "Users can read own agenda items"
        on public.learning_agenda_items for select to authenticated using (auth.uid() = user_id);
    end if;

    if not exists (
        select 1 from pg_policies
        where schemaname = 'public' and tablename = 'learning_agenda_items' and policyname = 'Users can insert own agenda items'
    ) then
        create policy "Users can insert own agenda items"
        on public.learning_agenda_items for insert to authenticated with check (auth.uid() = user_id);
    end if;

    if not exists (
        select 1 from pg_policies
        where schemaname = 'public' and tablename = 'learning_agenda_items' and policyname = 'Users can update own agenda items'
    ) then
        create policy "Users can update own agenda items"
        on public.learning_agenda_items for update to authenticated using (auth.uid() = user_id);
    end if;
end;
$$;
