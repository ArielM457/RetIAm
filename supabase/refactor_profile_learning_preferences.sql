-- Refactor incremental para dejar listas las preferencias reales del agente
-- de aprendizaje antes de generar rutas, planes y agenda.

alter table if exists public.profiles
    add column if not exists preferred_start_hour integer check (preferred_start_hour between 0 and 23),
    add column if not exists preferred_study_days text[] not null default '{}',
    add column if not exists content_preferences text[] not null default '{}',
    add column if not exists study_techniques text[] not null default '{}',
    add column if not exists learning_goals text[] not null default '{}',
    add column if not exists technology_experience text[] not null default '{}';

alter table if exists public.profile_assessments
    add column if not exists preferred_start_hour integer check (preferred_start_hour between 0 and 23),
    add column if not exists preferred_study_days text[] not null default '{}',
    add column if not exists content_preferences text[] not null default '{}',
    add column if not exists study_techniques text[] not null default '{}',
    add column if not exists learning_goals text[] not null default '{}',
    add column if not exists technology_experience text[] not null default '{}';

update public.profiles
set preferred_start_hour = case preferred_time
    when 'morning' then 8
    when 'afternoon' then 14
    when 'night' then 19
    else preferred_start_hour
end
where preferred_start_hour is null and preferred_time is not null;

update public.profile_assessments
set preferred_start_hour = case preferred_time
    when 'morning' then 8
    when 'afternoon' then 14
    when 'night' then 19
    else preferred_start_hour
end
where preferred_start_hour is null and preferred_time is not null;

update public.profiles
set preferred_study_days = case preferred_time
    when 'morning' then array['Monday', 'Thursday', 'Friday']
    when 'afternoon' then array['Tuesday', 'Thursday', 'Friday']
    when 'night' then array['Monday', 'Wednesday', 'Saturday']
    else preferred_study_days
end
where coalesce(array_length(preferred_study_days, 1), 0) = 0 and preferred_time is not null;

update public.profile_assessments
set preferred_study_days = case preferred_time
    when 'morning' then array['Monday', 'Thursday', 'Friday']
    when 'afternoon' then array['Tuesday', 'Thursday', 'Friday']
    when 'night' then array['Monday', 'Wednesday', 'Saturday']
    else preferred_study_days
end
where coalesce(array_length(preferred_study_days, 1), 0) = 0 and preferred_time is not null;
