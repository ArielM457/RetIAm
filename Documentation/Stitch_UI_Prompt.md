Diseña la interfaz completa de RetAIM, una plataforma SaaS de aprendizaje empresarial con IA para certificaciones técnicas en Azure, AWS y GitHub, orientada a empresas en LATAM. Tiene dos roles: employee y manager.

---

## NAVEGACIÓN PRINCIPAL

No usar sidebar. Usar SOLO navbar superior horizontal con:
- Logo RetAIM a la izquierda
- Pocas opciones de navegación en el centro (máximo 5 ítems, sin mega-menús)
- Avatar del usuario, notificaciones y CTA a la derecha
- Fondo de navbar con transparencia o color sólido oscuro
- Sin íconos decorativos en el nav, solo texto limpio con subrayado activo o pill de estado

Para employee el nav tiene: Inicio · Mi Plan · Sesiones · Certificados · Perfil
Para manager el nav tiene: Inicio · Equipo · Brechas · Resumen · Perfil

En mobile el nav colapsa en hamburger limpio.

---

## IDENTIDAD VISUAL

Paleta:
- #4F46E5 (índigo)
- #7C3AED (violeta)
- #2563EB (azul)
- #0F172A (fondo oscuro profundo)
- #000000
- #FFFFFF
- #E5E7EB (gris claro)

Fondos principales: gradientes amplios entre azul profundo, violeta y negro suave. Usar halos difusos de color como elemento atmosférico detrás del contenido, no como ruido visual.

Superficies de tarjetas: blancas con sombra suave, o negro/gris muy oscuro con bordes finos.

Acentos de acción: violeta eléctrico y azul brillante para botones primarios con gradiente.

Glassmorphism solo en modales y paneles flotantes del agente IA — no en cards generales.

---

## ESTILO GENERAL

Inspiración en la limpieza de Udemy pero con identidad visual premium propia:
- Layouts editoriales amplios con mucho espacio blanco o espacio oscuro limpio
- Contenido organizado en filas horizontales tipo "shelf", no en grids densos de tarjetas
- Jerarquía tipográfica muy marcada: títulos grandes, subtítulos medios, body compacto
- Pocos elementos por pantalla, cada uno con intención clara
- No usar decenas de tarjetas rectangulares apiladas — priorizar ritmo visual y respiración
- Fondos con gradientes amplios y halos, no colores planos
- Botones primarios con gradiente violeta→azul
- Botones secundarios outline o ghost
- Progress bars elegantes tipo línea fina con color degradado
- Pills de estado pequeños y concisos
- Tipografía fuerte en headings (tipo Inter, Plus Jakarta Sans o similar), body legible y limpio
- Nada recargado, nada infantil, nada barroco

---

## COMPONENTES CLAVE

### Cards de certificación / cursos:
Estilo tipo Udemy: imagen de portada amplia o ícono representativo, título, proveedor (Azure/AWS/GitHub), nivel, horas estimadas. Layout horizontal tipo shelf, no grid denso de tarjetas chicas.

### Chat del agente IA (dentro de sesiones):
Panel flotante lateral de ancho medio (~380px) que aparece sobre el contenido principal sin reemplazarlo. Estilo de ventana de chat moderna: burbujas, área de input fija abajo, cabecera con nombre del agente y avatar IA. Glassmorphism sutil en el fondo del panel. Se puede abrir/cerrar con un botón flotante. No ocupa toda la pantalla. En mobile se abre como bottom sheet deslizante.

### Dashboard cards:
Máximo 3-4 métricas visibles a la vez. Sin tablas de datos densas en el fold principal. Usar número grande + label pequeño + sparkline o mini barra.

### Progress:
Timeline semanal con línea horizontal y puntos de hito, sin tablas. Progress por sección con barra fina coloreada.

---

## PANTALLAS

### 1. Login / Registro
- Layout de dos columnas: izquierda con hero visual (gradiente + mensaje de valor), derecha con formulario limpio
- Tabs switch entre Iniciar sesión y Crear cuenta
- Campos: email, password, nombre completo, rol (employee / manager)
- CTA principal con gradiente
- Sin sidebar, sin nav en esta pantalla

### 2. Onboarding multipaso
- Stepper horizontal en la parte superior
- Un solo bloque de contenido centrado por paso, sin columnas
- Pasos: datos profesionales → disponibilidad horaria → estilo de aprendizaje → preguntas técnicas → nivel detectado + recomendaciones
- Pantalla final motivadora: nivel detectado, ruta sugerida, CTA para comenzar
- Tono guiado, simple y humano

### 3. Dashboard employee
- Saludo personalizado grande al inicio (tipo "Bienvenido de vuelta, Ariel")
- Una sección hero con: certificación actual, % de progreso, días al deadline, CTA de continuar
- Debajo: siguiente hito de la semana (simple, una línea con fecha y nombre)
- Fila horizontal de acciones rápidas: Generar recordatorios, Ver plan, Ver certificados
- Bloque de insight del sistema (1 sola sugerencia destacada, no lista)
- Estado del examen final (pill de estado claro)
- Esta pantalla debe ser la más atractiva del producto

### 4. Selección de certificación
- Navbar superior + filtros horizontales por categoría (Azure / AWS / GitHub / Todos)
- Shelf de certificaciones: fila horizontal scrolleable, tarjetas amplias con portada, título, nivel, horas
- Panel de detalle que aparece al hacer clic (drawer lateral o sección inferior), con descripción, temario y CTA para generar ruta
- Sin sidebar

### 5. Mi Plan
- Nombre de certificación + fecha límite + estado del plan arriba
- Timeline semanal horizontal con puntos de hito
- Lista de secciones con progreso por barra fina coloreada
- Días y horarios sugeridos en formato simple (no tabla densa)
- CTA para iniciar sesión del día

### 6. Sesión de aprendizaje
- Layout de dos columnas: contenido principal a la izquierda (recursos, pregunta, evaluación), panel del agente IA flotante a la derecha
- El panel del agente es una ventana de chat de ancho medio, con glassmorphism sutil, que se puede minimizar
- Encabezado de la sección, recursos recomendados (links o cards chicas), pregunta obligatoria, caja de respuesta
- Evaluación final y encuesta corta al finalizar
- Feedback de aprobado / needs retry al finalizar

### 7. Recordatorios
- Lista limpia de recordatorios con: tono, momento programado, estado (pill), contexto breve
- CTA para regenerar recordatorios
- Resumen del contexto sugerido por el sistema (bloque destacado al inicio)
- Sin tabla densa, formato tipo feed vertical

### 8. Examen final
- Pantalla full-focus: navbar minimal, sin distracciones
- Temporizador visible arriba
- Contador de pregunta actual / total
- Layout limpio para responder: una pregunta por pantalla, opciones claras
- Barra de progreso del examen
- Confirmación modal antes de enviar

### 9. Resultado de examen
Estado aprobado:
- Score grande y celebratorio, badge de certificado, botón descargar PDF, siguiente certificación sugerida

Estado no aprobado:
- Score con desglose, secciones a reforzar (lista simple), CTA para volver al plan

### 10. Perfil
- Layout de dos columnas: datos del usuario a la izquierda, configuraciones a la derecha
- Nombre, rol profesional, certificación actual, horas semanales, horario preferido, estilo de aprendizaje
- Botón de editar por sección, no un formulario general

### 11. Sugerencias (modal o drawer)
- Modal o panel deslizable: categoría, mensaje del sistema, estado de la sugerencia, feedback
- Accesible desde un botón flotante o desde el nav global

### 12. Dashboard manager
- Navbar superior igual al employee pero con ítems de manager
- Métricas ejecutivas principales: progreso promedio del equipo, miembros en riesgo, top gaps
- Formato limpio: 3-4 números grandes con contexto, no decenas de tarjetas
- Acceso rápido a resumen semanal y exportar PDF
- Tabla simple de equipo (no densa) con estado por fila

### 13. Equipo y miembros
- Lista de miembros con: foto/avatar, nombre, rol, certificación actual, progreso (barra fina), estado (pill)
- Invitaciones pendientes en un bloque separado
- CTA para invitar miembro, CTA para asignar certificación

### 14. Detalle de miembro
- Perfil del miembro: certificación, progreso, nivel de riesgo (color semáforo), días al deadline
- Secciones pendientes (lista simple)
- Botón para enviar mensaje de apoyo

### 15. Brechas del equipo
- Top 3 temas con más dificultad: visualización clara, no tabla densa
- Vista agregada con explicación visual simple (barras o íconos representativos)
- Sugerencia de acción grupal destacada

### 16. Resumen semanal (manager)
- Highlights del equipo en la semana
- Riesgos detectados (lista breve)
- Próximos vencimientos (timeline simple)
- Botón de exportar PDF visible y claro

---

## RESPONSIVE

Desktop: navbar horizontal, layouts de dos columnas donde aplica, content amplio
Tablet: navbar horizontal colapsada si es necesario, columnas reducidas a una
Mobile: hamburger menu, cards apiladas, panel del agente IA como bottom sheet, formularios cómodos, dashboards simplificados con las métricas más importantes al tope

---

## REGLAS FINALES

- Consistencia visual total entre todas las pantallas
- Respiración visual: pocos elementos por pantalla, bien espaciados
- No sidebar en ninguna pantalla — todo va en navbar superior
- No grids densos de tarjetas — usar shelfs horizontales o layouts editoriales amplios
- No tablas pesadas — solo listas limpias o tablas mínimas cuando sean necesarias
- Glassmorphism solo en el panel del agente IA y modales
- Gradientes en fondos y botones primarios, no en todo
- El resultado debe verse como un producto listo para demo de hackathon de alto nivel: coherente, moderno, elegante y claro