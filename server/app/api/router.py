from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.catalog import router as catalog_router
from app.api.routes.coach import router as coach_router
from app.api.routes.exams import router as exams_router
from app.api.routes.health import router as health_router
from app.api.routes.learning import router as learning_router
from app.api.routes.manager import router as manager_router
from app.api.routes.sessions import router as sessions_router
from app.api.routes.suggestions import router as suggestions_router
from app.api.routes.system import router as system_router
from app.api.routes.teams import router as teams_router
from app.api.routes.users import router as users_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(catalog_router, tags=["catalog"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(teams_router, prefix="/teams", tags=["teams"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(learning_router, prefix="/learning", tags=["learning"])
api_router.include_router(sessions_router, prefix="/sessions", tags=["sessions"])
api_router.include_router(coach_router, prefix="/coach", tags=["coach"])
api_router.include_router(manager_router, prefix="/manager", tags=["manager"])
api_router.include_router(exams_router, prefix="/exams", tags=["exams"])
api_router.include_router(suggestions_router, prefix="/suggestions", tags=["suggestions"])
api_router.include_router(system_router, prefix="/system", tags=["system"])
