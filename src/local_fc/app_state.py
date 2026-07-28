from dataclasses import dataclass

from local_fc.catalog_fetcher import CatalogFetcher
from local_fc.did_resolver import DidResolver
from local_fc.federated_collector import FederatedCollector
from local_fc.jsonld import JsonldParser
from local_fc.settings import Settings


@dataclass
class AppState:
    """State of the fastapi app."""

    settings: Settings
    catalog_fetcher: CatalogFetcher
    did_resolvers: DidResolver
    jsonld_parser: JsonldParser
    federated_collector: FederatedCollector
