from dataclasses import dataclass

from local_fc.edc_client import EdcClient
from local_fc.federated_collector import FederatedCollector
from local_fc.partner_mapping import PartnerMapping
from local_fc.settings import Settings


@dataclass
class AppState:
    """State of the fastapi app."""

    settings: Settings
    edc_client: EdcClient
    federated_collector: FederatedCollector
    partner_mapping: PartnerMapping
