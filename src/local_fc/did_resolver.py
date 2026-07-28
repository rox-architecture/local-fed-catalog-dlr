from typing import Any
from urllib.parse import unquote

from hishel.httpx import AsyncCacheClient

DID_NAMESPACE = "https://www.w3.org/ns/did"


def _did_web_to_url(did: str) -> str:
    """Return the URL for the given web DID."""
    prefix = "did:web:"
    if not did.startswith(prefix):
        error_message = f"Not a valid did:web identifier: {did}"
        raise ValueError(error_message)

    identifier = did[len(prefix) :]
    if not identifier:
        error_message = "Empty identifier after 'did:web:' prefix"
        raise ValueError(error_message)

    segments = [unquote(seg) for seg in identifier.split(":")]
    domain, path_segments = segments[0], segments[1:]

    if not domain:
        error_message = "Missing domain in did:web identifier"
        raise ValueError(error_message)

    if path_segments:
        path = "/".join(path_segments)
        return f"https://{domain}/{path}/did.json"
    return f"https://{domain}/.well-known/did.json"


class DidResolver:
    """Resolver for DID documents."""

    def __init__(self, *, timeout: int) -> None:
        """Initialize the instance."""
        self._client = AsyncCacheClient(
            follow_redirects=False,
            timeout=timeout,
        )

    async def resolve(self, did: str) -> dict[str, Any]:
        """Resolve the given DID."""
        url = _did_web_to_url(did)
        response = await self._client.get(url)
        response.raise_for_status()
        return response.json()

    async def shutdown(self) -> None:
        """Shut down the resolver."""
        await self._client.aclose()
