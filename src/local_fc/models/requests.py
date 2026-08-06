from local_fc.models.camel_case_model import CamelCaseModel


class NegotiationInitiationRequest(CamelCaseModel):
    """Negotiation initiation request model."""

    bpn: str
    asset_id: str
