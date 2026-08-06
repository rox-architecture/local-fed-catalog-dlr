from typing import Any

from fastapi import APIRouter

from local_fc.routers.common import State

agreements_router = APIRouter(prefix="/agreements", tags=["Agreements"])


@agreements_router.get("")
async def get_agreements(state: State) -> Any:
    """Return all agreements."""
    return await state.edc_client.get_agreements()
