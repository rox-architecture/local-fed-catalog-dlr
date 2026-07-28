from typing import Any, NamedTuple


class ExternalContext(NamedTuple):
    """An external JSON-LD context."""

    url: str
    content: dict[str, Any]
