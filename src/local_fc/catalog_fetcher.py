from typing import Any

from httpx import AsyncClient
from pydantic import HttpUrl

from local_fc.did_resolver import DID_NAMESPACE, DidResolver
from local_fc.jsonld import JsonldParser

EDC_CONTEXT = {
    "tx": "https://w3id.org/tractusx/v0.0.1/ns/",
    "tx-auth": "https://w3id.org/tractusx/auth/",
    "cx-policy": "https://w3id.org/catenax/2025/9/policy/",
    "@vocab": "https://w3id.org/edc/v0.0.1/ns/",
    "edc": "https://w3id.org/edc/v0.0.1/ns/",
    "odrl": "http://www.w3.org/ns/odrl/2/",
    "dcat": "http://www.w3.org/ns/dcat#",
    "dct": "http://purl.org/dc/terms/",
    "dspace": "https://w3id.org/dspace/v0.8/",
}

SERVICES_KEY = f"{DID_NAMESPACE}#service"
SERVICE_ENDPOINT_KEY = f"{DID_NAMESPACE}#serviceEndpoint"


def _get_service_identifier(service: dict[str, Any]) -> str | None:
    """Return the identifier of the given service."""
    url = service.get("@id")
    if not isinstance(url, str):
        return None

    parts = url.split("/")
    if len(parts) == 0:
        return None

    return parts[-1]


def _get_service_endpoint(service: dict[str, Any]) -> str | None:
    """Return the endpoint of the given service."""
    endpoints = service.get(SERVICE_ENDPOINT_KEY)
    if not isinstance(endpoints, list):
        return None
    if len(endpoints) == 0:
        return None

    endpoint = endpoints[0]
    if not isinstance(endpoint, dict):
        return None

    return endpoint.get("@id")


class CatalogFetcher:
    """Fetcher for catalogs."""

    def __init__(
        self,
        *,
        base_url: HttpUrl,
        api_key: str,
        did_resolver: DidResolver,
        jsonld_parser: JsonldParser,
        dsp_service_id: str,
        timeout: int,
    ) -> None:
        """Initialize the instance."""
        self._did_resolver = did_resolver
        self._jsonld_parser = jsonld_parser
        self._dsp_service_id = dsp_service_id

        headers = {"Authorization": f"Bearer {api_key}"}
        self._base_url = base_url
        self._client = AsyncClient(timeout=timeout, headers=headers)

    def _get_dsp_service_endpoint(self, did_document: dict[str, Any]) -> str | None:
        """Retrieve the DSP URL from the given expanded DID document."""
        services = did_document.get(SERVICES_KEY, [])

        for service in services:
            if _get_service_identifier(service) == self._dsp_service_id:
                return _get_service_endpoint(service)

        return None

    async def fetch(self, bpn: str, did: str, limit: int = 1000) -> Any:
        """Fetch the catalog of the given participant."""
        did_document = await self._did_resolver.resolve(did)
        expanded = self._jsonld_parser.expand(did_document)
        dsp_url = self._get_dsp_service_endpoint(expanded[0])

        if dsp_url is None:
            error_message = "Failed to fetch DSP URL"
            raise ValueError(error_message)

        url = f"{self._base_url}v3/catalog/request"
        payload = {
            "@context": EDC_CONTEXT,
            "counterPartyAddress": dsp_url,
            "counterPartyId": bpn,
            "protocol": "dataspace-protocol-http",
            "querySpec": {"offset": 0, "limit": limit},
        }

        response = await self._client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    async def shutdown(self) -> None:
        """Shut down the fetcher."""
        await self._client.aclose()
