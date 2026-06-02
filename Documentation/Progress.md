# Progress

## 2026-06-01

### Lo que hicimos hoy

- Inicializamos `server` con `FastAPI` y una estructura base en `app/api`, `app/core`, `app/db`, `app/models` y `app/services`.
- Dejamos configurada la conexion a Supabase para auth y base de datos desde backend.
- Agregamos validacion de correo corporativo para el MVP de la hackathon.
- Creamos el endpoint `GET /api/health`.
- Creamos el endpoint `POST /api/auth/validate-email`.
- Creamos el endpoint `GET /api/users/me` para sincronizar y leer el perfil autenticado.
- Inicializamos `client` con `Angular`.
- Configuramos `Tailwind CSS` en el frontend.
- Configuramos `Supabase Auth` en el frontend con flujo de login y registro.
- Dejamos un dashboard inicial protegido por sesion.
- Agregamos `supabase/schema.sql` con tablas base para organizaciones, perfiles, equipos y miembros.
- Agregamos `.gitignore` y ejemplos de configuracion para que el repo quede listo para subir.

### Archivos clave

- `server/.env.example`
- `server/app/main.py`
- `server/app/core/config.py`
- `server/app/core/security.py`
- `server/app/services/profile_service.py`
- `client/public/runtime-config.js`
- `client/src/app/core/auth/auth.store.ts`
- `client/src/app/core/services/api.service.ts`
- `client/src/app/features/auth/login-page/login-page.component.ts`
- `client/src/app/features/dashboard/dashboard-page.component.ts`
- `supabase/schema.sql`

### Verificaciones hechas

- `client` compila con `npm run build`
- `server` levanta con `uvicorn`
- `GET /api/health` responde `{"status":"ok"}`

### Configuracion pendiente para correr con datos reales

- Completar `server/.env` usando `server/.env.example`
- Completar `client/public/runtime-config.js` con `SUPABASE_URL`, `SUPABASE_ANON_KEY` y `apiBaseUrl`
- Ejecutar `supabase/schema.sql` en el proyecto real de Supabase
- Desactivar confirmacion por correo en Supabase Auth si queremos demo inmediata sin email

### Siguiente paso recomendado

- Implementar Epica 1 completa
- Crear organizaciones, equipos e invitaciones
- Definir pantalla de onboarding para Gini Profile
