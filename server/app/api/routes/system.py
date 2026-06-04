from fastapi import APIRouter

from app.models.integration import IntegrationStatusResponse
from app.services.integration_service import get_integration_status

router = APIRouter()


@router.get("/integrations/status", response_model=IntegrationStatusResponse)
def get_status() -> IntegrationStatusResponse:
    return get_integration_status()
