from fastapi import APIRouter, HTTPException, status

from local_fc.routers.common import State

partners_router = APIRouter(prefix="/partners", tags=["Partners"])


@partners_router.get("")
async def get_partners(state: State) -> dict[str, str]:
    """Return all partners."""
    return await state.partner_mapping.get_all()


@partners_router.post("")
async def add_partners(payload: dict[str, str], state: State) -> None:
    """Add the given partners."""
    try:
        await state.partner_mapping.add(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e


@partners_router.delete("")
async def remove_partners(payload: dict[str, str], state: State) -> None:
    """Add the given partners."""
    try:
        await state.partner_mapping.remove(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
