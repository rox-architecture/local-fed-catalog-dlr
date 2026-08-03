from typing import Any
from unittest.mock import AsyncMock

import httpx
import pytest
import respx
from pydantic import HttpUrl

from local_fc.catalog_fetcher import CatalogFetcher


@pytest.fixture
def did_resolver(did_document: dict[str, Any]) -> AsyncMock:
    """Return a mock DID resolver."""
    did_resolver = AsyncMock()
    did_resolver.resolve.return_value = did_document
    return did_resolver


@respx.mock
@pytest.mark.asyncio
async def test_fetch(did_resolver: AsyncMock) -> None:
    """Test catalog fetching."""
    base_url = HttpUrl("https://www.example.com/management")
    catalog_fetcher = CatalogFetcher(
        base_url=base_url,
        api_key="dummy",
        dsp_service_id="dsp-url",
        timeout=1,
    )
    catalog_fetcher._did_resolver = did_resolver

    url = "https://www.example.com/management/v3/catalog/request"
    content = {"@context": {}, "originator": "https://www.example.com/cp/protocol"}
    respx.post(url).mock(return_value=httpx.Response(200, json=content))

    catalog = await catalog_fetcher.fetch("BPNL000000000001", "did:web:www.example.com")

    assert catalog == content
