from fastapi import APIRouter

from local_fc.models.responses import HealthResponse

health_router = APIRouter(prefix="/health", tags=["Health"])


@health_router.get("")
async def get_health() -> HealthResponse:
    """Return the application health."""
    return HealthResponse()
