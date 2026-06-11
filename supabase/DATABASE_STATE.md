# Estado actual de la base de datos de RetAIM

Este archivo documenta como queda la base de datos despues de los refactors aplicados.

Objetivo:
- tener una referencia corta y humana del estado actual
- saber que archivo SQL ejecutar segun el momento
- actualizar este archivo cada vez que agreguemos nuevas tablas o relaciones

## Fuente de verdad

- Archivo completo del esquema actual: `supabase/schema.sql`
- Refactor incremental mas reciente: `supabase/refactor_profile_learning_preferences.sql`

Regla recomendada:
- `schema.sql` representa la foto completa de la base
- cada cambio nuevo que no requiera reinstalar todo debe salir en un archivo `refactor_*.sql`
- cuando agreguemos otro refactor, tambien actualizar este documento

## Refactors historicos

### 1. Refactor base ya aplicado

Ese refactor previo dejo lista la base para:
- equipos enriquecidos con `sector`, `member_capacity`, `work_style`, `notes`
- `team_access_codes`
- personalizacion de rutas y planes con `profile_context` y `personalization_summary`
- catalogo de cursos
- contenido por seccion, leccion y lab
- chat por leccion
- RAG con `pgvector` y `lesson_chunks`

### 2. Refactor de inscripcion y agenda

Archivo:
- `supabase/refactor_agenda_enrollment.sql`

Este agrega:
- `course_enrollments`
- `learning_agenda_items`
- indices y politicas RLS para ambos

### 3. Refactor incremental actual

Archivo a ejecutar ahora:
- `supabase/refactor_profile_learning_preferences.sql`

Este agrega:
- `preferred_start_hour`
- `preferred_study_days`
- `content_preferences`
- `study_techniques`
- `learning_goals`
- `technology_experience`

Lo agrega en:
- `profiles`
- `profile_assessments`

Ademas:
- rellena una hora inicial estimada para perfiles viejos segun `preferred_time`
- rellena dias sugeridos para perfiles viejos que aun no tenian preferencia explicita

## Modulos actuales de la base

### Identidad y organizacion

Tablas:
- `organizations`
- `profiles`
- `teams`
- `team_members`
- `team_invitations`
- `team_access_codes`

Uso:
- organiza usuarios, equipos, acceso por codigo y datos base del perfil

### Evaluacion inicial y personalizacion

Tablas:
- `profile_assessments`
- `learning_routes`
- `study_plans`

Uso:
- guarda la evaluacion inicial del usuario
- genera la ruta personalizada
- genera el plan progresivo

Campos clave:
- `learning_routes.profile_context`
- `learning_routes.personalization_summary`
- `study_plans.personalization_summary`
- `study_plans.weekly_milestones`
- `study_plans.workiq_context`
- `profiles.preferred_start_hour`
- `profiles.preferred_study_days`
- `profiles.study_techniques`
- `profiles.content_preferences`
- `profiles.learning_goals`
- `profiles.technology_experience`

### Curso y contenido

Tablas:
- `courses`
- `course_sections`
- `course_lessons`
- `course_labs`

Uso:
- catalogo real de cursos
- estructura completa del contenido ingerido desde Microsoft Learn o plantillas

### Progreso de aprendizaje

Tablas:
- `learning_sessions`
- `lesson_completions`
- `lesson_chat_messages`
- `integrity_events`
- `exam_attempts`
- `certificates`

Uso:
- seguimiento de sesiones
- completitud por leccion
- chat del tutor
- integridad
- examen final y certificados

### Recordatorios y soporte

Tablas:
- `coach_reminders`
- `suggestions`

Uso:
- recordatorios del coach
- brechas o sugerencias del usuario

### Inscripcion y agenda

Tablas:
- `course_enrollments`
- `learning_agenda_items`

Uso:
- `course_enrollments` guarda que curso eligio el usuario y con que ruta/plan activo quedo asociado
- `learning_agenda_items` guarda las sesiones, revisiones, labs, checkins y recordatorios por fecha

Campos clave en `course_enrollments`:
- `status`
- `activated_route_id`
- `activated_plan_id`
- `preferences_snapshot`
- `personalization_summary`
- `current_section_id`
- `current_session_id`

Campos clave en `learning_agenda_items`:
- `item_type`
- `related_session_id`
- `related_section_id`
- `related_lesson_ids`
- `scheduled_start`
- `scheduled_end`
- `agenda_date`
- `status`
- `metadata`

### RAG del tutor

Tablas y objetos:
- `lesson_chunks`
- funcion `match_lesson_chunks`
- extension `vector`

Uso:
- grounding del tutor con fragmentos reales del contenido

## Relaciones importantes

- `profiles.id` se relaciona con casi todo lo que es del usuario
- `courses.id` se relaciona con `course_sections`
- `course_sections.id` se relaciona con `course_lessons` y `course_labs`
- `learning_routes.id` se relaciona con `study_plans`
- `study_plans.id` se relaciona con `learning_sessions`
- `course_enrollments` conecta usuario, curso, ruta y plan
- `learning_agenda_items` conecta usuario, inscripcion, ruta y plan

## Estado funcional esperado

Con la base actual, RetAIM ya deberia poder:
- mostrar catalogo real de cursos
- inscribir al usuario a un curso
- generar ruta personalizada
- generar plan progresivo
- guardar agenda por fechas
- guardar sesiones y chat por leccion
- usar RAG en el tutor

## Cuando actualizar este documento

Actualizar este archivo si cambiamos cualquiera de estas cosas:
- nuevas tablas
- nuevas columnas estructurales
- nuevas relaciones
- nuevos modulos funcionales
- nuevos refactors SQL

## Siguiente convención sugerida

Para futuros cambios usar nombres como:
- `refactor_calendar_reschedule.sql`
- `refactor_learning_unlocks.sql`
- `refactor_manager_analytics.sql`

Y luego agregar una seccion nueva aqui indicando:
- que agrega
- si depende de un refactor anterior
- que archivo se debe ejecutar
