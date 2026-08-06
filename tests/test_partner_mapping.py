import json
from pathlib import Path

import pytest

from local_fc.partner_mapping import PartnerMapping


@pytest.mark.asyncio
async def test_get_all(tmp_path: Path) -> None:
    """Test retrieval of the full mapping."""
    path = tmp_path / "partners.json"
    entries = {"1": "2", "3": "4"}

    partner_mapping = PartnerMapping(path)
    path.write_text(json.dumps(entries))

    assert await partner_mapping.get_all() == entries


@pytest.mark.asyncio
async def test_add(tmp_path: Path) -> None:
    """Test adding of entries."""
    path = tmp_path / "partners.json"
    entries = {"1": "2", "3": "4"}

    partner_mapping = PartnerMapping(path)
    await partner_mapping.add(entries)

    assert await partner_mapping.get_all() == entries


@pytest.mark.asyncio
async def test_remove(tmp_path: Path) -> None:
    """Test removal of entries."""
    path = tmp_path / "partners.json"
    entries = {"1": "2", "3": "4"}

    partner_mapping = PartnerMapping(path)
    path.write_text(json.dumps(entries))
    await partner_mapping.remove(entries)

    assert await partner_mapping.get_all() == {}
