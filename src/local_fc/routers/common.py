from typing import Annotated

from fastapi import Depends, Request

from local_fc.app_state import AppState


def _get_state(request: Request) -> AppState:
    return request.app.state.app_state


State = Annotated[AppState, Depends(_get_state)]
