from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from local_fc.app_state import AppState
from local_fc.edc_client import EdcClient
from local_fc.federated_collector import FederatedCollector
from local_fc.partner_mapping import PartnerMapping
from local_fc.routers import routers
from local_fc.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Handle startup and shutdown events."""
    settings = Settings()
    edc_client = EdcClient(
        base_url=settings.connector_management_api,
        api_key=settings.connector_api_key,
        dsp_service_id=settings.dsp_service_id,
        timeout=settings.edc_client_timeout_seconds,
    )
    partner_mapping = PartnerMapping(settings.partner_mapping_path)
    federated_collector = FederatedCollector(
        edc_client=edc_client,
        partner_mapping=partner_mapping,
        poll_interval=settings.federated_collector_poll_interval_seconds,
        concurrency=settings.federated_collector_concurreny_max,
        retries=settings.federated_collector_retries_max,
        delay=settings.federated_collector_retries_delay_seconds,
    )

    app.state.app_state = AppState(
        settings=settings,
        edc_client=edc_client,
        federated_collector=federated_collector,
        partner_mapping=partner_mapping,
    )

    await federated_collector.start()

    yield

    await federated_collector.shutdown()
    await edc_client.shutdown()


app = FastAPI(title="Local Federated Catalog", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers:
    app.include_router(router)
