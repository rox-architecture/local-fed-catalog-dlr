from typing import Any
from unittest.mock import AsyncMock

import httpx
import pytest
import respx
from pydantic import HttpUrl

from local_fc.edc_client import EdcClient


@pytest.fixture
def did_resolver(did_document: dict[str, Any]) -> AsyncMock:
    """Return a mock DID resolver."""
    did_resolver = AsyncMock()
    did_resolver.resolve.return_value = did_document
    return did_resolver


@respx.mock
@pytest.mark.asyncio
async def test_get_catalog(did_resolver: AsyncMock) -> None:
    """Test catalog fetching."""
    base_url = HttpUrl("https://www.example.com/management")
    edc_client = EdcClient(
        base_url=base_url,
        api_key="dummy",
        dsp_service_id="dsp-url",
        timeout=1,
    )
    edc_client._did_resolver = did_resolver

    url = "https://www.example.com/management/v3/catalog/request"
    content = {"@context": {}, "originator": "https://www.example.com/cp/protocol"}
    respx.post(url).mock(return_value=httpx.Response(200, json=content))

    catalog = await edc_client.get_catalog(
        "BPNL000000000001", "did:web:www.example.com"
    )

    assert catalog == content


@respx.mock
@pytest.mark.asyncio
async def test_get_agreements() -> None:
    """Test agreement fetching."""
    base_url = HttpUrl("https://www.example.com/management")
    edc_client = EdcClient(
        base_url=base_url,
        api_key="dummy",
        dsp_service_id="dsp-url",
        timeout=1,
    )

    url = "https://www.example.com/management/v3/contractagreements/request"
    content = ["a", "b"]
    respx.post(url).mock(return_value=httpx.Response(200, json=content))

    agreements = await edc_client.get_agreements()

    assert agreements == content


@respx.mock
@pytest.mark.asyncio
async def test_initiate_negotiation() -> None:
    """Test negotiation initiation."""
    base_url = HttpUrl("https://www.example.com/management")
    edc_client = EdcClient(
        base_url=base_url,
        api_key="dummy",
        dsp_service_id="dsp-url",
        timeout=1,
    )

    url = "https://www.example.com/management/v3/edrs"
    content = {}
    respx.post(url).mock(return_value=httpx.Response(200, json=content))

    response = await edc_client.initiate_negotiation("a", "b")

    assert response == content
