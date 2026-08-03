import asyncio
import json
from pathlib import Path
from typing import Any


class JsonStore:
    """An async-safe store for a JSON file."""

    _INDENT = 4

    def __init__(self, path: Path) -> None:
        """Initialize the instance."""
        self._path = path
        self._lock = asyncio.Lock()

    def read(self) -> Any:
        """Return the contents of the JSON file using a sync operation."""
        if not self._path.exists():
            return None
        return json.loads(self._path.read_text())

    def write(self, contents: Any) -> None:
        """Write the given contents of the JSON file using a sync operation."""
        tmp = self._path.with_suffix(".tmp")
        tmp.write_text(json.dumps(contents, indent=self._INDENT))
        tmp.replace(self._path)

    async def aread(self) -> Any:
        """Return the contents of the JSON file using an async operation."""
        async with self._lock:
            return await asyncio.to_thread(self.read)

    async def awrite(self, contents: Any) -> Any:
        """Return the contents of the JSON file using an async operation."""
        async with self._lock:
            return await asyncio.to_thread(self.write, contents)
