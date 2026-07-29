from fastapi import APIRouter

from local_fc.routers.common import State

trigger_router = APIRouter(prefix="/trigger", tags=["Trigger"])


@trigger_router.get("")
async def trigger_refresh(state: State) -> None:
    """Trigger a refresh of the federated catalog."""
    await state.federated_collector.trigger()
