import asyncio
from unittest.mock import AsyncMock

import pytest

from local_fc.federated_collector import FederatedCollector


@pytest.fixture
def edc_client() -> AsyncMock:
    """Return a mock EDC client."""
    edc_client = AsyncMock()
    edc_client.get_catalog.return_value = {"@context": {}}
    return edc_client


@pytest.fixture
def partner_mapping() -> AsyncMock:
    """Return a mock catalog fetcher."""
    partner_mapping = AsyncMock()
    partner_mapping.get_all.return_value = {"1": "2"}
    return partner_mapping


@pytest.mark.asyncio
async def test_fetch(edc_client: AsyncMock, partner_mapping: AsyncMock) -> None:
    """Test catalog fetching."""
    federated_collector = FederatedCollector(
        edc_client=edc_client,
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
