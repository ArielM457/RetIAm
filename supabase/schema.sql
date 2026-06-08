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
    professional_role text,
    org_id uuid references public.organizations (id) on delete set null,
    team_id uuid,
    target_certification text,
    detected_level text check (detected_level in ('basic', 'intermediate', 'advanced')),
    weekly_hours_available integer,
    preferred_time text check (preferred_time in ('morning', 'afternoon', 'night')),
    learning_style text[] not null default '{}',
    profile_version integer not null default 1,
    onboarding_completed_at timestamptz,
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

create table if not exists public.team_invitations (
    id uuid primary key default gen_random_uuid(),
    team_id uuid not null references public.teams (id) on delete cascade,
    org_id uuid not null references public.organizations (id) on delete cascade,
    email text not null,
    role text not null default 'employee' check (role in ('manager', 'employee')),
    status text not null default 'pending' check (status in ('pending', 'accepted', 'cancelled')),
    invited_by uuid not null references public.profiles (id) on delete cascade,
    accepted_by uuid references public.profiles (id) on delete set null,
    invited_at timestamptz not null default timezone('utc', now()),
    responded_at timestamptz
);

create unique index if not exists team_invitations_team_email_idx
on public.team_invitations (team_id, email);

create table if not exists public.profile_assessments (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.profiles (id) on delete cascade,
    professional_role text not null,
    target_certification text not null,
    detected_level text not null check (detected_level in ('basic', 'intermediate', 'advanced')),
    weekly_hours_available integer not null,
    preferred_time text not null check (preferred_time in ('morning', 'afternoon', 'night')),
    learning_style text[] not null default '{}',
    questions jsonb not null default '[]'::jsonb,
    answers jsonb not null default '[]'::jsonb,
    score integer not null default 0,
    max_score integer not null default 0,
    notes text,
    created_at timestamptz not null default timezone('utc', now())
);

create table if not exists public.learning_routes (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.profiles (id) on delete cascade,
    target_certification text not null,
    detected_level text not null check (detected_level in ('basic', 'intermediate', 'advanced')),
    sections jsonb not null default '[]'::jsonb,
    source_mode text not null default 'mock' check (source_mode in ('mock', 'foundry')),
    created_at timestamptz not null default timezone('utc', now())
);

create table if not exists public.study_plans (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.profiles (id) on delete cascade,
    route_id uuid not null references public.learning_routes (id) on delete cascade,
    target_certification text not null,
    deadline_at timestamptz not null,
    weekly_hours integer not null,
    weekly_milestones jsonb not null default '[]'::jsonb,
    workiq_context jsonb not null default '{}'::jsonb,
    status text not null default 'active' check (status in ('active', 'completed', 'paused', 'needs_reinforcement')),
    created_at timestamptz not null default timezone('utc', now()),
    updated_at timestamptz not null default timezone('utc', now())
);

create table if not exists public.team_certification_assignments (
    id uuid primary key default gen_random_uuid(),
    team_id uuid not null references public.teams (id) on delete cascade,
    assigned_by uuid not null references public.profiles (id) on delete cascade,
    target_certification text not null,
    member_ids jsonb not null default '[]'::jsonb,
    created_at timestamptz not null default timezone('utc', now())
);

create table if not exists public.learning_sessions (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.profiles (id) on delete cascade,
    plan_id uuid not null references public.study_plans (id) on delete cascade,
    section_id text not null,
    section_title text not null,
    session_type text not null check (session_type in ('theory', 'practice', 'quiz', 'lab')),
    status text not null default 'in_progress' check (status in ('in_progress', 'completed', 'needs_retry')),
    resources jsonb not null default '[]'::jsonb,
    mandatory_question jsonb,
    free_questions jsonb not null default '[]'::jsonb,
    evaluation jsonb not null default '{}'::jsonb,
    survey jsonb,
    started_at timestamptz not null default timezone('utc', now()),
    completed_at timestamptz
);

create table if not exists public.integrity_events (
    id uuid primary key default gen_random_uuid(),
    session_id uuid not null references public.learning_sessions (id) on delete cascade,
    user_id uuid not null references public.profiles (id) on delete cascade,
    event_type text not null,
    payload jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default timezone('utc', now())
);

create table if not exists public.coach_reminders (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.profiles (id) on delete cascade,
    plan_id uuid references public.study_plans (id) on delete cascade,
    kind text not null check (kind in ('standard', 'deadline', 'minimal')),
    tone text not null default 'formal' check (tone in ('formal', 'casual', 'concise')),
    delivery_channel text not null default 'platform' check (delivery_channel in ('platform', 'teams')),
    message text not null,
    scheduled_for timestamptz not null,
    status text not null default 'scheduled' check (status in ('scheduled', 'sent', 'dismissed')),
    created_at timestamptz not null default timezone('utc', now())
);

create table if not exists public.exam_attempts (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.profiles (id) on delete cascade,
    plan_id uuid not null references public.study_plans (id) on delete cascade,
    target_certification text not null,
    questions jsonb not null default '[]'::jsonb,
    answers jsonb not null default '[]'::jsonb,
    time_limit_minutes integer not null default 60,
    score integer not null default 0,
    max_score integer not null default 0,
    passed boolean not null default false,
    failed_sections jsonb not null default '[]'::jsonb,
    recommendations jsonb not null default '[]'::jsonb,
    next_certification text,
    started_at timestamptz not null default timezone('utc', now()),
    submitted_at timestamptz
);

alter table public.exam_attempts add column if not exists time_limit_minutes integer not null default 60;
alter table public.exam_attempts add column if not exists failed_sections jsonb not null default '[]'::jsonb;
alter table public.exam_attempts add column if not exists recommendations jsonb not null default '[]'::jsonb;
alter table public.exam_attempts add column if not exists next_certification text;

create table if not exists public.certificates (
    id text primary key,
    user_id uuid not null references public.profiles (id) on delete cascade,
    recipient_name text,
    target_certification text not null,
    score integer not null,
    pdf_url text,
    verification_code text not null,
    issued_at timestamptz not null default timezone('utc', now())
);

alter table public.certificates add column if not exists recipient_name text;

create table if not exists public.suggestions (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.profiles (id) on delete cascade,
    team_id uuid references public.teams (id) on delete set null,
    category text not null check (category in ('content', 'interface', 'pace', 'other')),
    message text not null,
    status text not null check (status in ('applicable', 'needs_context', 'queued')),
    agent_response text not null,
    created_at timestamptz not null default timezone('utc', now()),
    reviewed_at timestamptz
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
alter table public.team_invitations enable row level security;
alter table public.profile_assessments enable row level security;
alter table public.learning_routes enable row level security;
alter table public.study_plans enable row level security;
alter table public.team_certification_assignments enable row level security;
alter table public.learning_sessions enable row level security;
alter table public.integrity_events enable row level security;
alter table public.coach_reminders enable row level security;
alter table public.exam_attempts enable row level security;
alter table public.certificates enable row level security;
alter table public.suggestions enable row level security;

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

create policy "Users can read own assessments"
on public.profile_assessments
for select
to authenticated
using (auth.uid() = user_id);

create policy "Users can insert own assessments"
on public.profile_assessments
for insert
to authenticated
with check (auth.uid() = user_id);

create policy "Users can read own routes"
on public.learning_routes
for select
to authenticated
using (auth.uid() = user_id);

create policy "Users can insert own routes"
on public.learning_routes
for insert
to authenticated
with check (auth.uid() = user_id);

create policy "Users can read own plans"
on public.study_plans
for select
to authenticated
using (auth.uid() = user_id);

create policy "Users can insert own plans"
on public.study_plans
for insert
to authenticated
with check (auth.uid() = user_id);

create policy "Users can read own learning sessions"
on public.learning_sessions
for select
to authenticated
using (auth.uid() = user_id);

create policy "Users can insert own learning sessions"
on public.learning_sessions
for insert
to authenticated
with check (auth.uid() = user_id);

create policy "Users can read own reminders"
on public.coach_reminders
for select
to authenticated
using (auth.uid() = user_id);

create policy "Users can read own exams"
on public.exam_attempts
for select
to authenticated
using (auth.uid() = user_id);

create policy "Users can insert own exams"
on public.exam_attempts
for insert
to authenticated
with check (auth.uid() = user_id);

create policy "Users can read own certificates"
on public.certificates
for select
to authenticated
using (auth.uid() = user_id);

create policy "Users can read own suggestions"
on public.suggestions
for select
to authenticated
using (auth.uid() = user_id);

create policy "Users can insert own suggestions"
on public.suggestions
for insert
to authenticated
with check (auth.uid() = user_id);

-- =====================================================================
-- Course content catalog (Fase 0 del modulo de cursos)
-- Contenido global (no por usuario) poblado por ingesta MS Learn / plantillas.
-- Jerarquia: courses -> course_sections -> course_lessons / course_labs.
-- =====================================================================

create table if not exists public.courses (
    id uuid primary key default gen_random_uuid(),
    certification_code text not null,
    track text not null check (track in ('azure', 'aws', 'github')),
    title text not null,
    summary text,
    provider text,
    level text not null default 'basic' check (level in ('basic', 'intermediate', 'advanced')),
    total_duration_minutes integer not null default 0,
    source text not null default 'template' check (source in ('template', 'ms_learn', 'synthetic')),
    source_url text,
    created_at timestamptz not null default timezone('utc', now()),
    updated_at timestamptz not null default timezone('utc', now())
);

create unique index if not exists courses_certification_code_idx
on public.courses (certification_code);

create table if not exists public.course_sections (
    id uuid primary key default gen_random_uuid(),
    course_id uuid not null references public.courses (id) on delete cascade,
    section_key text not null,
    title text not null,
    summary text,
    "order" integer not null default 1,
    duration_minutes integer not null default 0,
    created_at timestamptz not null default timezone('utc', now()),
    unique (course_id, section_key)
);

create table if not exists public.course_lessons (
    id uuid primary key default gen_random_uuid(),
    section_id uuid not null references public.course_sections (id) on delete cascade,
    lesson_key text not null,
    title text not null,
    "order" integer not null default 1,
    duration_minutes integer not null default 0,
    content_md text,
    learning_objectives jsonb not null default '[]'::jsonb,
    sources jsonb not null default '[]'::jsonb,
    created_at timestamptz not null default timezone('utc', now()),
    unique (section_id, lesson_key)
);

create table if not exists public.course_labs (
    id uuid primary key default gen_random_uuid(),
    section_id uuid not null references public.course_sections (id) on delete cascade,
    lesson_id uuid references public.course_lessons (id) on delete set null,
    lab_key text not null,
    title text not null,
    is_optional boolean not null default true,
    estimated_minutes integer not null default 30,
    instructions_md text,
    rubric jsonb not null default '[]'::jsonb,
    created_at timestamptz not null default timezone('utc', now()),
    unique (section_id, lab_key)
);

-- Progreso por leccion (por usuario)
create table if not exists public.lesson_completions (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.profiles (id) on delete cascade,
    plan_id uuid references public.study_plans (id) on delete cascade,
    lesson_id uuid not null references public.course_lessons (id) on delete cascade,
    session_id uuid references public.learning_sessions (id) on delete set null,
    status text not null default 'completed' check (status in ('in_progress', 'completed')),
    completed_at timestamptz not null default timezone('utc', now()),
    unique (user_id, lesson_id)
);

-- Chat del tutor por leccion (Gini Eval)
create table if not exists public.lesson_chat_messages (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.profiles (id) on delete cascade,
    lesson_id uuid not null references public.course_lessons (id) on delete cascade,
    session_id uuid references public.learning_sessions (id) on delete set null,
    role text not null check (role in ('user', 'assistant')),
    content text not null,
    sources jsonb not null default '[]'::jsonb,
    suggested_questions jsonb not null default '[]'::jsonb,
    source_mode text not null default 'mock' check (source_mode in ('mock', 'foundry')),
    created_at timestamptz not null default timezone('utc', now())
);

create index if not exists lesson_chat_messages_lookup_idx
on public.lesson_chat_messages (user_id, lesson_id, created_at);

alter table public.courses enable row level security;
alter table public.course_sections enable row level security;
alter table public.course_lessons enable row level security;
alter table public.course_labs enable row level security;
alter table public.lesson_completions enable row level security;
alter table public.lesson_chat_messages enable row level security;

-- El catalogo de cursos es contenido global legible por cualquier usuario autenticado.
create policy "Authenticated can read courses"
on public.courses for select to authenticated using (true);

create policy "Authenticated can read course sections"
on public.course_sections for select to authenticated using (true);

create policy "Authenticated can read course lessons"
on public.course_lessons for select to authenticated using (true);

create policy "Authenticated can read course labs"
on public.course_labs for select to authenticated using (true);

create policy "Users can read own lesson completions"
on public.lesson_completions for select to authenticated using (auth.uid() = user_id);

create policy "Users can insert own lesson completions"
on public.lesson_completions for insert to authenticated with check (auth.uid() = user_id);

create policy "Users can read own lesson chat"
on public.lesson_chat_messages for select to authenticated using (auth.uid() = user_id);

create policy "Users can insert own lesson chat"
on public.lesson_chat_messages for insert to authenticated with check (auth.uid() = user_id);

-- =====================================================================
-- RAG con pgvector (Supabase como base vectorial)
-- Reemplaza a Azure AI Search: el tutor recupera fragmentos reales del
-- contenido completo de las lecciones y los pasa como contexto a GPT-4o.
-- Dimension 1024 = BGE-M3 / multilingual-e5-large.
-- =====================================================================

create extension if not exists vector;

create table if not exists public.lesson_chunks (
    id uuid primary key default gen_random_uuid(),
    certification_code text not null,
    lesson_key text not null,
    lesson_title text,
    content text not null,
    source_url text,
    chunk_index integer not null default 0,
    embedding vector(1024),
    created_at timestamptz not null default timezone('utc', now())
);

create index if not exists lesson_chunks_cert_idx
on public.lesson_chunks (certification_code, lesson_key);

create index if not exists lesson_chunks_embedding_idx
on public.lesson_chunks using hnsw (embedding vector_cosine_ops);

alter table public.lesson_chunks enable row level security;

create policy "Authenticated can read lesson chunks"
on public.lesson_chunks for select to authenticated using (true);

-- Busqueda por similitud (cosine). filter_certification = busca dentro del curso.
create or replace function public.match_lesson_chunks(
    query_embedding vector(1024),
    match_count int default 5,
    filter_certification text default null
)
returns table (
    id uuid,
    certification_code text,
    lesson_key text,
    lesson_title text,
    content text,
    source_url text,
    similarity float
)
language sql stable
as $$
    select
        lc.id,
        lc.certification_code,
        lc.lesson_key,
        lc.lesson_title,
        lc.content,
        lc.source_url,
        1 - (lc.embedding <=> query_embedding) as similarity
    from public.lesson_chunks lc
    where filter_certification is null or lc.certification_code = filter_certification
    order by lc.embedding <=> query_embedding
    limit match_count;
$$;
