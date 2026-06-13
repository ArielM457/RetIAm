# Team Lead — Curso personalizado (Fase 1)

El team lead puede crear un **curso a medida** para su equipo (temas que no son una
certificación de Microsoft, o un recorte de un curso). Sube/pega un **Markdown**, la IA lo
organiza en la estructura estándar, valida los **mínimos** para ser certificable, lo guarda
**visible solo para su equipo** y genera **embeddings en el pgvector** para que el tutor pueda
responder dudas de ese tema (RAG), igual que con los cursos de Microsoft Learn.

## Cómo se usa
1. Manager → menú **"Curso a medida"** (`/manager/custom-course`).
2. Elige el **equipo**, pega el **Markdown** (o sube `.md`/`.txt`), opcionalmente un título.
3. **Previsualizar** → ve la estructura + si es certificable + qué falta.
4. **Crear curso** → se publica para el equipo y se indexa para el RAG.

## Formato del Markdown
```
# Título del curso
Resumen breve (opcional).

## Sección 1: Fundamentos
### Lección 1.1: Conceptos
Contenido en Markdown de la lección…

#### Lab: Práctica guiada   (opcional)
Instrucciones del laboratorio…

## Sección 2: …
### Lección 2.1: …
```
- `#` = título del curso · `##` = sección · `###` = lección · `#### Lab:` = laboratorio.
- La IA (`gpt-4.1-mini`) normaliza el texto a la estructura; si no hay IA, un **parser
  determinista** por encabezados hace el respaldo (funciona offline).

## Mínimos para ser "certificable" (recomendados)
- **3+ secciones**, **3+ lecciones**, **1+ laboratorio**, todas las lecciones con contenido,
  y **≥ 60 min** de duración estimada.
- Si no cumple, se guarda igual como **borrador** (no certificable) y se listan los pendientes.
- Examen de certificación (en tiempo de examen): **10 preguntas, aprueba con 70%**.

## Qué se construyó (y qué se reutilizó)
- **Reutilizado:** `course_service.upsert_course` (persiste curso→secciones→lecciones→labs),
  `embedding_service.embed_documents` + `rag_service.upsert_lesson_chunks` (RAG), patrón de
  agente del panel de manager.
- **Nuevo backend:** `services/custom_course_service.py` (normalización IA + parser de
  respaldo + validación + guardado + embeddings), rutas
  `POST /api/manager/teams/{team_id}/custom-courses[/preview]`.
- **Nuevo frontend:** `features/manager/manager-custom-course-page.component.ts` + ruta
  `/manager/custom-course` + link "Curso a medida" en el shell de manager.

## Mejoras añadidas sobre la idea original (documentadas)
1. **Scoping real por equipo:** el catálogo (`list_courses`) ahora filtra — los cursos
   personalizados solo los ven los miembros del equipo (vía `team_service.get_user_team_ids`).
   Columnas nuevas en `courses`: `team_id`, `created_by`, `visibility`, `is_certifiable`.
2. **Previsualizar antes de crear**, con "gate" de certificable + lista de pendientes, para
   que el lead corrija antes de publicar.
3. **Parser determinista de respaldo**: funciona aunque la IA externa esté apagada.
4. **Duraciones estimadas** automáticamente por longitud de contenido (~180 palabras/min).
5. **Código de certificación** auto-generado y único (`TEAM-XXXXXX`), provider
   "Plataforma RetIAm", `track='custom'`, `source='custom'`.

## Requisitos para que funcione
- **Re-correr `supabase/schema.sql`** en el SQL Editor (agrega columnas/constraints nuevos de
  `courses`; es idempotente).
- **Reiniciar el backend** (rutas nuevas + scoping del catálogo).
- Para el RAG del curso, `fastembed` instalado (ya está); los embeddings corren local.

## Ranking con agente (Fase 2)
Manager → **"Ranking"** (`/manager/insights`). Un agente (`gpt-4o`) cruza datos reales y muestra:
- **Top performer** (score = progreso·0.5 + aprobación·0.3 + sesiones·4),
- **Récord de tiempo** (quién completa una sección más rápido, de `learning_sessions`),
- **Mejor metodología** (estilo de aprendizaje con mejor progreso promedio),
- un **insight redactado por el agente** + tabla de ranking.
- Backend: `services/ranking_service.py`, ruta `GET /api/manager/teams/{id}/ranking`.

## Asignar y notificar (Fase 3)
- **Asignar** ya estaba completo: `assign_certification_to_team` crea ruta + plan, fija
  `target_certification` y **notifica** (sirve también para cursos personalizados, mismo código).
- **Notificar (mejorado):**
  - Se corrigió un **bug**: `send_support_message` insertaba `kind='manager_support'`, que
    violaba el CHECK de `coach_reminders`. Se **relajó el CHECK** (`manager_support`, `nudge`).
  - **Nudge con IA** a un miembro: `POST /api/manager/teams/{id}/members/{member_id}/nudge`
    (si no mandas texto, la IA lo redacta según su progreso/riesgo).
  - **Aviso masivo a los en riesgo**: botón en `/manager/insights` →
    `POST /api/manager/teams/{id}/nudge-at-risk` (la IA redacta a cada uno).

## Limitaciones conocidas / futuro
- `GET /api/courses/{code}` no está restringido por equipo (el **listado** sí lo oculta, pero
  el detalle por código directo no valida pertenencia). Endurecer si se requiere.
- PDF/DOCX no se parsean: el upload acepta texto/Markdown.
- El ranking usa duración de sesión (completed_at − started_at); si una sesión se marca
  completada al instante, su "récord" puede ser muy bajo. Afinar con un mínimo si hace falta.
