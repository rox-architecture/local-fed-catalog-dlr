from typing import Any

import pyld

from local_fc.jsonld.did_v1 import did_v1
from local_fc.jsonld.external_context import ExternalContext


class CachedContextLoader:
    """Context loader for cached external JSON-LD contexts."""

    def __init__(self, contexts: list[ExternalContext]) -> None:
        """Initialize the instance."""
        self._contexts = {context.url: context.content for context in contexts}

    def __call__(self, url: str, _: Any = None) -> dict[str, Any]:
        """Resolve the given external context."""
        content = self._contexts.get(url)

        if content is None:
            error_message = f"Unknown context: {url}"
            raise pyld.jsonld.JsonLdError(error_message, "UnknownContext")

        return {
            "contentType": "application/ld+json",
            "contextUrl": None,
            "documentUrl": url,
            "document": content,
        }


class JsonldParser:
    """Parser for JSON-LD documents."""

    VOCAB = "https://w3id.org/edc/v0.0.1/ns/"

    def __init__(self) -> None:
        """Initialize the instance."""
        self._loader = CachedContextLoader([did_v1])

    def expand(self, document: dict[str, Any]) -> list[Any]:
        """Expand the given document."""
        return pyld.jsonld.expand(document, {"documentLoader": self._loader})
