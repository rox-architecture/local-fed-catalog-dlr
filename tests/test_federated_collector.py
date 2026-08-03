import asyncio
from unittest.mock import AsyncMock

import pytest

from local_fc.federated_collector import FederatedCollector


@pytest.fixture
def catalog_fetcher() -> AsyncMock:
    """Return a mock catalog fetcher."""
    catalog_fetcher = AsyncMock()
    catalog_fetcher.fetch.return_value = {"@context": {}}
    return catalog_fetcher


@pytest.fixture
def partner_mapping() -> AsyncMock:
    """Return a mock catalog fetcher."""
    partner_mapping = AsyncMock()
    partner_mapping.get_all.return_value = {"1": "2"}
    return partner_mapping


@pytest.mark.asyncio
async def test_fetch(catalog_fetcher: AsyncMock, partner_mapping: AsyncMock) -> None:
    """Test catalog fetching."""
    federated_collector = FederatedCollector(
        catalog_fetcher=catalog_fetcher,
        partner_mapping=partner_mapping,
        poll_interval=0.005,
        concurrency=10,
        retries=3,
        delay=0.001,
    )

    await federated_collector.start()
    await asyncio.sleep(0.01)

    catalogs = federated_collector.get_catalogs()

    await federated_collector.shutdown()

    assert catalogs == [{"@context": {}}]
