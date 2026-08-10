from typing import Any

from fastapi import APIRouter, HTTPException, status

from local_fc.models.requests import NegotiationInitiationRequest
from local_fc.routers.common import State

negotiations_router = APIRouter(prefix="/negotiations", tags=["Negotiations"])


@negotiations_router.post("")
async def initiate_negotiation(
    payload: NegotiationInitiationRequest, state: State
) -> Any:
    """Initiate a negotiation."""
    catalogs = state.federated_collector.get_catalogs()

    catalog = next(
        (item for item in catalogs if item["dspace:participantId"] == payload.bpn),
        None,
    )
    if catalog is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Catalog not found")

    originator = catalog["originator"]
    datasets = catalog["dcat:dataset"]
    if not isinstance(datasets, list):
        datasets = [datasets]

    dataset = next((item for item in datasets if item["@id"] == payload.asset_id), None)
    if dataset is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Dataset not found")

    policies = dataset["odrl:hasPolicy"]
    if not isinstance(policies, list):
        policies = [policies]

    return await state.edc_client.initiate_negotiation(originator, policies[0])
