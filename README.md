# RetAIM — AI-Powered Certification Training Platform

> Retain Objectives with AI — Plataforma de capacitación técnica para equipos en LATAM

---

## Qué es RetAIM

RetAIM es una plataforma de aprendizaje empresarial con agentes de IA que ayuda a empresas en LATAM a certificar equipos técnicos en Azure, AWS y GitHub de manera rápida, personalizada y medible. El sistema adapta cada plan de estudio al nivel real y disponibilidad de cada persona, y le da al manager visibilidad completa del progreso del equipo.

Construido para la Agents League Hackathon 2026, RetAIM integra Foundry IQ como base de conocimiento fundamentada y Work IQ como capa de contexto laboral, ejecutando un equipo de agentes especializados llamados Gini sobre Azure AI Foundry Agent Service.

> **Nota:** Todos los datos de usuarios, equipos y certificaciones usados en esta demo son completamente sintéticos. No contienen información personal identificable real.

---

## El problema que resuelve

Las empresas en LATAM que quieren certificar a sus equipos técnicos no tienen forma de saber quién está listo, quién necesita más tiempo, ni cuándo estudiar sin interrumpir el trabajo. Los managers no tienen visibilidad y los empleados no tienen un plan adaptado a su carga real. Los errores son costosos: tiempo perdido, exámenes fallidos y certificaciones vencidas sin que nadie lo note a tiempo.

---

## Microsoft IQ integrados

### Foundry IQ
Es la base de conocimiento de RetAIM. Ahí viven los documentos de certificaciones técnicas en formato sintético indexados con Azure AI Search. Cuando Gini Path sugiere una ruta o Gini Eval genera una pregunta de evaluación, cita directamente de esa base. Eso garantiza que las respuestas estén fundamentadas en contenido aprobado y no en conocimiento genérico del modelo.

### Work IQ
Es la capa de contexto laboral. Gini Coach lee las señales de Microsoft 365 de cada empleado, sus reuniones y sus bloques de concentración disponibles, para decidir cuándo y cómo enviar recordatorios. No interrumpe en medio de una reunión. Adapta el ritmo de estudio al ritmo de trabajo real de cada persona.

---

## Stack técnico

| Capa | Tecnología |
|------|-----------|
| Agentes | Azure AI Foundry Agent Service (hosted) |
| Modelo | GPT-4o-mini |
| Base de conocimiento | Foundry IQ + Azure AI Search + Azure Blob Storage |
| Backend | Python (FastAPI) en Azure Container Apps |
| Base de datos | Supabase (PostgreSQL) |
| Frontend | Angular + Tailwind CSS en Azure Static Web Apps |
| Integración Teams | Work IQ + Copilot Studio |
| Infraestructura | Azure CLI scripts (provisioning automatizado) |
| Voz | Azure AI Speech (dictado en evaluaciones) |

---

## Los agentes Gini

### Gini Router
Orquestador central. Recibe toda solicitud desde Teams o la plataforma y decide qué agente especializado activar. No responde directamente al usuario, solo coordina el flujo.

### Gini Profile
Hace la evaluación inicial de cada empleado cuando entra por primera vez. Evalúa su rol, nivel actual en el área de certificación elegida y disponibilidad horaria semanal. Construye el perfil base que usan todos los demás agentes.

### Gini Path
Toma el perfil del empleado y la certificación objetivo, consulta la base de Foundry IQ y devuelve una ruta de aprendizaje con secciones ordenadas y recursos citados de documentación real. Nunca inventa contenido.

### Gini Planner
Convierte la ruta de Gini Path en un plan con fechas, hitos semanales y fecha de vencimiento. Toma en cuenta las horas disponibles del perfil y las señales de Work IQ para armar un calendario realista. Una fecha de vencimiento siempre está presente porque es lo que genera compromiso real.

### Gini Coach
Agente de acompañamiento continuo. Manda recordatorios adaptativos, avisa cuando se acerca una fecha de vencimiento y ajusta el tono según el patrón del usuario. Aprende si la persona prefiere mensajes cortos o resúmenes detallados.

### Gini Eval
Evaluador de sesión. Al final de cada bloque de contenido hace una pregunta obligatoria fundamentada en lo que el usuario leyó, responde dudas libres, califica labs y quizzes para pasar de sección y genera el examen final de certificación. Si la nota no alcanza, devuelve al usuario a Gini Planner para reforzar.

### Gini Insight
Agente de retroalimentación y automejora. Después de cada sesión hace una encuesta corta, registra cómo aprendió mejor el usuario y actualiza su perfil de aprendizaje para adaptar las siguientes sesiones. Evalúa sugerencias del usuario y decide si son aplicables o las encola para revisión.

### Gini Lens
Agente del manager. Muestra el estado del equipo, quién avanza, quién está en riesgo de no llegar a su fecha de vencimiento y qué áreas tienen más brechas. Presenta la información de forma agregada, sin exponer datos personales sensibles de cada empleado.

---

## Flujo principal del sistema

```
Empleado entra a RetAIM
        ↓
Gini Profile → Evaluación inicial de nivel y disponibilidad
        ↓
Gini Path → Ruta de certificación fundamentada en Foundry IQ
        ↓
Gini Planner → Plan con fechas y vencimiento (Work IQ signals)
        ↓
Sesión de aprendizaje:
  → Contenido citado (Foundry IQ)
  → Pregunta obligatoria + dudas libres (Gini Eval)
  → Lab o quiz para pasar sección
  → Encuesta de sesión (Gini Insight)
        ↓
Gini Coach → Recordatorios adaptativos entre sesiones
        ↓
Examen final → Certificación RetAIM
        ↓
Gini Lens → Manager ve progreso del equipo completo
```

---

## Estructura del repositorio

```
retaim/
├── infra/                  # Scripts de Azure CLI para provisioning
│   ├── provision.sh        # Script maestro que crea todos los servicios
│   ├── foundry.sh          # Crea proyecto Foundry + knowledge base
│   ├── container_apps.sh   # Crea Azure Container Apps para el backend
│   ├── static_web.sh       # Crea Azure Static Web Apps para el frontend
│   └── agents/             # Scripts que crean cada agente Gini en Foundry
│       ├── create_agents.py
│       └── agent_configs/  # JSON de configuración de cada agente
├── backend/                # FastAPI Python
│   ├── app/
│   │   ├── agents/         # Integración con Foundry Agent Service
│   │   ├── api/            # Rutas REST
│   │   ├── models/         # Modelos de datos
│   │   └── services/       # Lógica de negocio
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # Angular + Tailwind
│   ├── src/
│   │   ├── app/
│   │   │   ├── auth/       # Login mock con correo corporativo
│   │   │   ├── dashboard/  # Dashboard empleado y manager
│   │   │   ├── courses/    # Flujo de sesión de aprendizaje
│   │   │   └── agents/     # Servicio de comunicación con agentes
│   └── staticwebapp.config.json
├── synthetic-data/         # Datos sintéticos para demo
│   ├── certifications/     # Documentos de certificaciones (AZ-900, AZ-204, etc.)
│   ├── users/              # Perfiles sintéticos de empleados
│   └── teams/              # Equipos y organizaciones ficticias
└── README.md
```

---

## Cómo levantar el proyecto

### Prerrequisitos
- Azure CLI instalado y cuenta con suscripción activa
- Python 3.11+
- Node.js 20+
- Angular CLI

### Provisioning de infraestructura

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/retaim
cd retaim

# Hacer login en Azure
az login

# Ejecutar script maestro de provisioning
# Este script crea todos los servicios de Azure y los agentes Gini automáticamente
chmod +x infra/provision.sh
./infra/provision.sh
```

El script crea en orden:
1. Resource Group en Azure
2. Azure AI Foundry Hub y Project
3. Knowledge base en Foundry IQ con los documentos sintéticos
4. Los 8 agentes Gini en Foundry Agent Service
5. Azure Container Apps para el backend
6. Azure Static Web Apps para el frontend
7. Variables de entorno necesarias

### Backend local

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # Completar con las variables del provisioning
uvicorn app.main:app --reload
```

### Frontend local

```bash
cd frontend
npm install
ng serve
```

---

## Datos sintéticos

Todos los perfiles, equipos, empresas y resultados de aprendizaje son ficticios y creados únicamente para propósitos de demostración. Los identificadores usan el formato `EMP-001`, `TEAM-A`, `ORG-LATAM-01`. No se incluye información personal real en ningún archivo del repositorio.

---

## Criterios de la hackathon cubiertos

| Criterio | Cobertura |
|----------|-----------|
| Precisión y relevancia | Sistema multiagente alineado al escenario del desafío |
| Razonamiento multi-paso | Gini Router orquesta 7 agentes especializados con flujo de decisión claro |
| Creatividad y originalidad | Aplicado a certificaciones técnicas en LATAM con contexto laboral real |
| Experiencia de usuario | Demo funcional en Teams + plataforma web Angular |
| Confiabilidad y seguridad | Foundry IQ fundamenta respuestas con citas, Gini Eval no adivina |
| Integración Microsoft IQ | Foundry IQ + Work IQ activos en el flujo principal |

---

## Equipo

Construido para la Agents League Hackathon 2026 — Reasoning Agents track.
