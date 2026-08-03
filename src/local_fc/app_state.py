from dataclasses import dataclass

from local_fc.catalog_fetcher import CatalogFetcher
from local_fc.federated_collector import FederatedCollector
from local_fc.partner_mapping import PartnerMapping
from local_fc.settings import Settings


@dataclass
class AppState:
    """State of the fastapi app."""

    settings: Settings
    catalog_fetcher: CatalogFetcher
    federated_collector: FederatedCollector
    partner_mapping: PartnerMapping
