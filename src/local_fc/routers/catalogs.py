from typing import Any

from fastapi import APIRouter

from local_fc.routers.common import State

catalogs_router = APIRouter(prefix="/catalogs", tags=["Catalogs"])


@catalogs_router.get("")
async def get_catalogs(state: State) -> list[Any]:
    """Return the federated catalog."""
    return state.federated_collector.get_catalogs()
