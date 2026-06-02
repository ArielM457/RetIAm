# RetAIM — Historias de usuario por épica

> Todas las historias siguen el formato: **Como [rol], quiero [acción], para [beneficio].**
> Prioridad: 🔴 Alta (MVP hackathon) · 🟡 Media · 🟢 Nice to have

---

## Épica 1 — Autenticación y gestión de equipos

Esta épica cubre el acceso a la plataforma, la creación de organizaciones y la gestión de equipos con roles diferenciados entre manager y empleado.

---

**US-101** 🔴
Como empleado, quiero ingresar a RetAIM con mi correo corporativo (mock), para acceder a mi plan de aprendizaje personalizado.

*Criterios de aceptación:*
- El sistema valida que el correo tenga formato de dominio corporativo (no gmail, hotmail, etc.)
- Si el correo no existe, muestra un mensaje de registro
- El login es mock: no requiere proveedor de identidad real en la demo

---

**US-102** 🔴
Como manager, quiero crear un equipo dentro de mi organización, para gestionar el aprendizaje de mis colaboradores desde un solo lugar.

*Criterios de aceptación:*
- Puedo darle nombre al equipo y agregar miembros por correo
- Al crear el equipo quedo asignado automáticamente como manager
- Puedo tener más de un equipo activo

---

**US-103** 🔴
Como manager, quiero invitar empleados a mi equipo, para que puedan comenzar su proceso de certificación dentro del grupo.

*Criterios de aceptación:*
- Los empleados reciben una notificación de invitación
- Solo los empleados con correo corporativo válido pueden unirse
- El empleado puede pertenecer a un solo equipo a la vez

---

**US-104** 🟡
Como empleado, quiero ver los demás miembros de mi equipo, para saber con quiénes comparto el proceso de aprendizaje.

*Criterios de aceptación:*
- Veo nombre, rol y certificación actual de cada compañero
- No veo métricas detalladas de otros empleados, solo su estado general

---

**US-105** 🟡
Como manager, quiero poder cambiar el rol de un miembro del equipo, para ajustar permisos si alguien pasa a liderar un subgrupo.

---

## Épica 2 — Perfil de aprendizaje y evaluación inicial (Gini Profile)

Esta épica cubre la evaluación que hace Gini Profile al primer ingreso de cada empleado para construir su perfil base de aprendizaje.

---

**US-201** 🔴
Como empleado nuevo en RetAIM, quiero que el sistema me haga una evaluación inicial de nivel, para que mi plan de estudio parta de donde realmente estoy y no desde cero.

*Criterios de aceptación:*
- Gini Profile me hace entre 5 y 10 preguntas sobre mi rol, experiencia y área de certificación
- Al finalizar genera un perfil con nivel detectado (básico, intermedio, avanzado)
- El perfil queda guardado y lo puedo consultar en cualquier momento

---

**US-202** 🔴
Como empleado, quiero declarar mi disponibilidad horaria semanal, para que mi plan de estudio sea realista y no me pida más horas de las que tengo.

*Criterios de aceptación:*
- Puedo indicar cuántas horas por semana tengo disponibles
- Puedo indicar en qué momentos del día prefiero estudiar (mañana, tarde, noche)
- Esta información la usa Gini Planner para armar el calendario

---

**US-203** 🔴
Como empleado, quiero indicar cómo aprendo mejor, para que el sistema adapte el formato de mis sesiones desde el inicio.

*Criterios de aceptación:*
- Puedo elegir entre opciones como: leer documentación, ver ejemplos de código, hacer ejercicios prácticos
- Gini Insight actualiza esta preferencia automáticamente con el tiempo según mi comportamiento

---

**US-204** 🟡
Como empleado, quiero poder actualizar mi perfil de aprendizaje manualmente, para corregir información que haya cambiado desde mi evaluación inicial.

---

**US-205** 🟢
Como manager, quiero ver el perfil de nivel de cada miembro de mi equipo, para entender las brechas de habilidades que hay en el grupo antes de asignar certificaciones.

---

## Épica 3 — Rutas y planes de certificación (Gini Path + Gini Planner)

Esta épica cubre la generación de rutas de aprendizaje personalizadas y la construcción del plan con fechas y vencimiento.

---

**US-301** 🔴
Como empleado, quiero elegir una certificación técnica objetivo (AZ-900, AZ-204, AWS Cloud Practitioner, etc.), para que el sistema me arme una ruta de aprendizaje específica para esa certificación.

*Criterios de aceptación:*
- El catálogo muestra las certificaciones disponibles con descripción y nivel requerido
- Gini Path consulta Foundry IQ y devuelve una ruta con secciones ordenadas
- Cada sección tiene los recursos citados de documentación real

---

**US-302** 🔴
Como empleado, quiero que mi plan de estudio tenga una fecha de vencimiento clara, para tener un compromiso real con mis objetivos de certificación.

*Criterios de aceptación:*
- Gini Planner calcula la fecha de vencimiento según mis horas disponibles y la duración estimada
- La fecha es visible en mi dashboard en todo momento
- Recibo alertas cuando me acerco al vencimiento

---

**US-303** 🔴
Como empleado, quiero que mi plan esté dividido en hitos semanales, para saber exactamente qué tengo que completar cada semana.

*Criterios de aceptación:*
- El plan muestra qué secciones corresponden a cada semana
- Puedo ver mi avance semanal en tiempo real
- Si me atraso, Gini Planner reajusta el plan automáticamente

---

**US-304** 🟡
Como empleado, quiero que mi plan tome en cuenta mis reuniones de la semana en Microsoft 365, para que no me asigne sesiones de estudio en momentos donde no puedo concentrarme.

*Criterios de aceptación:*
- Work IQ lee las señales de calendario del usuario
- Gini Planner evita bloques de estudio durante reuniones densas
- El usuario puede sobrescribir la sugerencia si quiere

---

**US-305** 🟡
Como manager, quiero poder asignar una certificación obligatoria a todo mi equipo, para alinear el desarrollo técnico del grupo hacia un objetivo común.

*Criterios de aceptación:*
- Puedo seleccionar una certificación y asignarla a uno o varios miembros
- Cada miembro recibe una notificación con la asignación
- El plan de cada miembro se genera de forma independiente según su perfil

---

**US-306** 🟢
Como empleado, quiero poder iniciar una segunda certificación en paralelo, para no quedarme bloqueado mientras espero terminar la primera.

---

## Épica 4 — Sesiones de aprendizaje (Gini Eval + Gini Insight)

Esta épica cubre el flujo de cada sesión individual: contenido, interacción con el agente, validación y retroalimentación.

---

**US-401** 🔴
Como empleado, quiero que cada sesión de aprendizaje me entregue contenido con referencias a documentación oficial, para saber que lo que estoy leyendo es confiable y está fundamentado.

*Criterios de aceptación:*
- Gini Eval entrega entre 2 y 4 recursos por sesión (links, fragmentos citados)
- Cada recurso tiene su fuente indicada (nombre del documento de Foundry IQ)
- No se entregan más de 4 recursos para no saturar al usuario

---

**US-402** 🔴
Como empleado, quiero que al final de cada bloque de contenido haya al menos una pregunta obligatoria del agente, para asegurarme de haber entendido lo que leí antes de continuar.

*Criterios de aceptación:*
- Gini Eval hace mínimo 1 pregunta fundamentada en el contenido de la sesión
- Si no respondo correctamente, el agente me explica la respuesta correcta con la cita correspondiente
- No puedo avanzar a la siguiente sección sin responder la pregunta obligatoria

---

**US-403** 🔴
Como empleado, quiero poder hacerle preguntas libres al agente sobre el contenido que no entendí, para no quedarme con dudas antes de avanzar.

*Criterios de aceptación:*
- Gini Eval responde preguntas libres en cualquier momento de la sesión
- Las respuestas siempre citan la fuente de Foundry IQ
- El agente me indica si la pregunta está fuera del alcance del contenido actual

---

**US-404** 🔴
Como empleado, quiero que para pasar de sección tenga que aprobar un quiz o un laboratorio práctico, para validar que realmente aprendí antes de avanzar.

*Criterios de aceptación:*
- Las secciones teóricas tienen un quiz de 3 a 5 preguntas calificadas por Gini Eval
- Las secciones prácticas tienen un laboratorio donde presento mi solución implementada
- La nota mínima para pasar es configurable (default 70%)
- Si no paso, puedo reintentar después de repasar el contenido

---

**US-405** 🔴
Como empleado, quiero que la IA califique mi laboratorio y me dé retroalimentación, para saber exactamente qué estuvo bien y qué necesito mejorar.

*Criterios de aceptación:*
- Gini Eval revisa la solución del laboratorio y asigna una nota con justificación
- La retroalimentación es específica y cita los criterios evaluados
- El resultado queda guardado en mi historial de aprendizaje

---

**US-406** 🟡
Como empleado, quiero que al final de cada sesión haya una encuesta corta sobre cómo fue mi experiencia de aprendizaje, para que el sistema mejore mis próximas sesiones.

*Criterios de aceptación:*
- La encuesta tiene máximo 3 preguntas (no más para no cansar al usuario)
- Gini Insight procesa las respuestas y actualiza mi perfil de preferencias
- Puedo saltar la encuesta si tengo poco tiempo, pero el sistema lo registra

---

**US-407** 🟡
Como empleado, quiero que el sistema detecte si aprendo mejor con cierto formato de contenido y lo priorice, para que cada sesión sea más efectiva que la anterior.

*Criterios de aceptación:*
- Gini Insight analiza mis respuestas y mi tiempo en cada tipo de contenido
- Actualiza mi perfil de aprendizaje automáticamente
- Los cambios se reflejan en la siguiente sesión sin que yo tenga que hacer nada

---

**US-408** 🟢
Como empleado, quiero que el sistema detecte si cambié de pestaña durante una evaluación, para que mis resultados sean una representación honesta de lo que sé.

*Criterios de aceptación:*
- Durante evaluaciones y exámenes, el sistema monitorea si salgo de la pestaña activa
- Si detecto un cambio de pestaña, registro el evento y notifico al manager
- Implementado como mock de AI Vision para la demo

---

## Épica 5 — Acompañamiento y recordatorios (Gini Coach)

Esta épica cubre el sistema de recordatorios adaptativos y seguimiento continuo del progreso del empleado.

---

**US-501** 🔴
Como empleado, quiero recibir recordatorios de estudio que se adapten a mi horario real, para que me ayuden a mantener el ritmo sin interrumpirme en momentos de alta carga de trabajo.

*Criterios de aceptación:*
- Gini Coach usa las señales de Work IQ para elegir el momento del recordatorio
- No envía recordatorios durante bloques de reuniones consecutivas
- Los recordatorios llegan por Teams o notificación de la plataforma

---

**US-502** 🔴
Como empleado, quiero recibir una alerta cuando mi fecha de vencimiento esté cerca, para tomar acción a tiempo y no perder mi objetivo de certificación.

*Criterios de aceptación:*
- Alerta cuando quedan 7 días para el vencimiento
- Alerta cuando quedan 3 días
- Alerta el día del vencimiento si el curso no está completado

---

**US-503** 🟡
Como empleado, quiero que el tono de los recordatorios se adapte a mi patrón de respuesta, para que sean más efectivos y menos repetitivos.

*Criterios de aceptación:*
- Si ignoro recordatorios formales, Gini Coach prueba un tono más casual
- Si respondo mejor a resúmenes cortos, los recordatorios son más concisos
- El sistema aprende en máximo 3 sesiones cuál tono funciona mejor

---

**US-504** 🟢
Como empleado, quiero poder configurar en qué días y horarios prefiero recibir recordatorios, para tener control sobre cuándo el sistema me contacta.

---

## Épica 6 — Dashboard del manager (Gini Lens)

Esta épica cubre la visibilidad que tiene el manager sobre el progreso de su equipo.

---

**US-601** 🔴
Como manager, quiero ver en un dashboard el estado general de mi equipo, para saber de un vistazo quién está avanzando y quién necesita atención.

*Criterios de aceptación:*
- El dashboard muestra cada miembro del equipo con su certificación actual y porcentaje de avance
- Indica en verde / amarillo / rojo el riesgo de no llegar a la fecha de vencimiento
- Se actualiza en tiempo real

---

**US-602** 🔴
Como manager, quiero ver qué empleados están en riesgo de no completar su certificación a tiempo, para poder intervenir antes de que sea demasiado tarde.

*Criterios de aceptación:*
- Gini Lens identifica automáticamente a empleados con riesgo alto basándose en su ritmo de avance vs días restantes
- Puedo hacer clic en un empleado para ver más detalle sin ver sus notas específicas
- Puedo enviarle un mensaje de apoyo directamente desde el dashboard

---

**US-603** 🟡
Como manager, quiero ver qué áreas de conocimiento tienen más brechas en mi equipo, para planificar capacitaciones grupales donde sea necesario.

*Criterios de aceptación:*
- Gini Lens agrupa los errores frecuentes por tema dentro de las certificaciones del equipo
- Muestra los 3 temas con más dificultad del equipo en el último mes
- Los datos son anónimos a nivel individual

---

**US-604** 🟡
Como manager, quiero recibir un resumen semanal del progreso de mi equipo por Teams, para estar informado sin tener que entrar a la plataforma todos los días.

*Criterios de aceptación:*
- Gini Lens envía un resumen los lunes con el estado del equipo
- El resumen incluye: avances de la semana anterior, alertas de riesgo y próximos vencimientos
- Puedo desactivar el resumen automático si prefiero revisarlo manualmente

---

**US-605** 🟢
Como manager, quiero exportar el reporte de progreso del equipo en PDF, para compartirlo con la dirección de la empresa en reuniones de seguimiento.

---

## Épica 7 — Examen final y certificación (Gini Eval)

Esta épica cubre el proceso de evaluación final para obtener la certificación RetAIM al completar un curso.

---

**US-701** 🔴
Como empleado, quiero que al completar todas las secciones de un curso haya un examen final, para validar de forma integral todo lo que aprendí.

*Criterios de aceptación:*
- El examen final tiene entre 15 y 25 preguntas generadas por Gini Eval desde Foundry IQ
- Las preguntas cubren todas las secciones del curso de forma proporcional
- Hay un tiempo límite configurable (default 60 minutos)

---

**US-702** 🔴
Como empleado, quiero saber mi resultado del examen final inmediatamente después de terminarlo, para saber si obtuve mi certificación o necesito reforzar.

*Criterios de aceptación:*
- Gini Eval califica el examen en tiempo real y muestra la nota al finalizar
- Si paso (default 70%), se genera el certificado RetAIM
- Si no paso, Gini Planner me indica qué secciones reforzar antes de reintentar

---

**US-703** 🟡
Como empleado, quiero que mi certificado RetAIM tenga un identificador único verificable, para poder compartirlo en LinkedIn o presentarlo ante mi empresa.

*Criterios de aceptación:*
- El certificado tiene un ID único generado al momento de la aprobación
- Incluye nombre del empleado (sintético en demo), certificación, fecha y puntuación final
- Se puede descargar en PDF

---

**US-704** 🟢
Como empleado, quiero que el sistema me recomiende la siguiente certificación una vez que aprobé la actual, para seguir avanzando en mi desarrollo técnico sin perder el momentum.

---

## Épica 8 — Infraestructura y provisioning automatizado

Esta épica cubre la creación automatizada de todos los servicios de Azure y los agentes Gini mediante scripts de Azure CLI.

---

**US-801** 🔴
Como desarrollador del equipo, quiero que toda la infraestructura de Azure se cree con un solo script, para poder levantar el entorno completo en minutos sin pasos manuales.

*Criterios de aceptación:*
- `provision.sh` crea el Resource Group, Foundry Hub, Container Apps y Static Web Apps
- El script tiene manejo de errores y muestra progreso en consola
- Al terminar imprime las URLs y variables de entorno necesarias

---

**US-802** 🔴
Como desarrollador del equipo, quiero que los 8 agentes Gini se creen automáticamente en Foundry Agent Service mediante un script Python, para no tener que configurarlos uno por uno desde la UI.

*Criterios de aceptación:*
- `create_agents.py` lee los archivos de configuración JSON de cada agente
- Crea cada agente con su system prompt, herramientas y conexión a Foundry IQ
- Confirma que todos los agentes quedaron activos al finalizar

---

**US-803** 🔴
Como desarrollador del equipo, quiero que los documentos sintéticos de certificaciones se indexen automáticamente en Foundry IQ, para que la base de conocimiento esté lista sin pasos manuales adicionales.

*Criterios de aceptación:*
- El script de provisioning sube los archivos de `synthetic-data/certifications/` a Blob Storage
- Crea el índice de Azure AI Search y lo conecta a Foundry IQ
- El proceso completo tarda menos de 10 minutos

---

**US-804** 🟡
Como desarrollador del equipo, quiero que exista un script de limpieza que elimine todos los recursos de Azure creados, para evitar costos innecesarios después de la demo.

---

## Épica 9 — Sugerencias del usuario y mejora continua (Gini Insight)

Esta épica cubre el sistema por el cual los usuarios pueden sugerir mejoras y el agente evalúa su aplicabilidad.

---

**US-901** 🟡
Como empleado, quiero poder dejar una sugerencia de mejora sobre el contenido o la experiencia de aprendizaje, para contribuir a que la plataforma sea mejor para todos.

*Criterios de aceptación:*
- Hay un botón de sugerencia accesible desde cualquier sesión
- Gini Insight evalúa la sugerencia y determina si es aplicable, si necesita revisión o si queda en cola
- El usuario recibe una respuesta del agente indicando qué pasará con su sugerencia

---

**US-902** 🟡
Como manager, quiero ver un resumen de las sugerencias que hicieron los miembros de mi equipo, para tener visibilidad sobre qué aspectos de la plataforma les generan fricción.

*Criterios de aceptación:*
- Gini Lens agrega las sugerencias del equipo por categoría (contenido, interfaz, ritmo)
- No muestra qué empleado hizo cada sugerencia específica
- El manager puede marcar sugerencias como prioritarias para elevarlas

---

**US-903** 🟢
Como empleado, quiero saber cuándo una sugerencia mía fue implementada o considerada, para sentir que mi aporte tiene valor real en la plataforma.
