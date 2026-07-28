from typing import Any

from local_fc.jsonld import JsonldParser


def test_expand(did_document: dict[str, Any]) -> None:
    """Test expanding JSON-LD documents."""
    expected_keys = {
        "@id",
        "https://w3id.org/security#authenticationMethod",
        "https://www.w3.org/ns/did#service",
        "https://w3id.org/security#verificationMethod",
    }
    parser = JsonldParser()

    parsed = parser.expand(did_document)

    assert len(parsed) == 1
    assert set(parsed[0].keys()) == expected_keys
