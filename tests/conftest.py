import json
from pathlib import Path
from typing import Any

import pytest

DATA_DIRECTORY = Path(__file__).parent / "data"


@pytest.fixture
def did_document() -> dict[str, Any]:
    """Return an example DID document."""
    path = DATA_DIRECTORY / "did_document.json"
    return json.loads(path.read_text())
