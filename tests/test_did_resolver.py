import httpx
import pytest
import respx

from local_fc.did_resolver import DidResolver


@respx.mock
@pytest.mark.asyncio
async def test_web_did() -> None:
    """Test resolution of web DIDs."""
    did = "did:web:www.example.com"
    resolver = DidResolver(timeout=1)

    url = "https://www.example.com/.well-known/did.json"
    content = {"id": 1, "name": "Alice"}
    respx.get(url).mock(return_value=httpx.Response(200, json=content))

    result = await resolver.resolve(did)
    await resolver.shutdown()

    assert result == content
