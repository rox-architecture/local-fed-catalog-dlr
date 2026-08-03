from pathlib import Path
from typing import cast

from local_fc.json_store import JsonStore


class PartnerMapping:
    """A mapping of participant BPNs to DIDs."""

    def __init__(self, path: Path) -> None:
        """Initialize the instance."""
        self._store = JsonStore(path)

        if not path.exists():
            self._store.write({})

    async def get_all(self) -> dict[str, str]:
        """Return the full mapping."""
        return cast("dict[str, str]", await self._store.aread())

    async def add(self, entries: dict[str, str]) -> None:
        """Add the given entries to the mapping."""
        contents = await self.get_all()

        if contents.keys() & entries.keys():
            error_message = "Conflict in participant mapping entries"
            raise ValueError(error_message)

        await self._store.awrite(contents | entries)

    async def remove(self, entries: dict[str, str]) -> None:
        """Remove the given entries to the mapping."""
        contents = await self.get_all()

        if contents.keys() < entries.keys():
            error_message = "Conflict in participant mapping entries"
            raise ValueError(error_message)

        for key in entries:
            contents.pop(key)

        await self._store.awrite(contents)
