import asyncio
import contextlib
import logging
from typing import Any

from local_fc.catalog_fetcher import CatalogFetcher

logger = logging.getLogger(__name__)


class FederatedCollector:
    """Collector for the federated catalog."""

    def __init__(
        self,
        *,
        catalog_fetcher: CatalogFetcher,
        poll_interval: float,
        concurrency: int,
        retries: int,
        delay: float,
    ) -> None:
        """Initialize the instance."""
        self._catalog_fetcher = catalog_fetcher
        self._poll_interval = poll_interval
        self._concurrency = concurrency
        self._retries = retries
        self._delay = delay

        self._catalogs = {}
        self._task: asyncio.Task[None] | None = None
        self._stop_event = asyncio.Event()

    async def _fetch_with_retry(self, bpn: str, did: str) -> None:
        """Fetch the given catalog with retry."""
        attempt = 0

        while True:
            attempt += 1
            try:
                catalog = await self._catalog_fetcher.fetch(bpn, did)
            except Exception:
                logger.exception("Failed to fetch catalog for %s", bpn)
                if attempt > self._retries:
                    return
                await asyncio.sleep(self._delay)
                continue

            self._catalogs[bpn] = catalog
            return

    async def _fetch_single_round(self) -> None:
        """Fetch each catalog once."""
        logger.info("Fetching catalogs")

        # TODO: Implement proper retrieval
        bpn_did_dict = {
            "BPNLD6VP3E63ZBUT": "did:web:vision-x-api.base-x-ecosystem.org:connectors:alice-http"
        }

        semaphore = asyncio.Semaphore(self._concurrency)

        async def _bounded_fetch(bpn: str, did: str) -> None:
            async with semaphore:
                await self._fetch_with_retry(bpn, did)

        await asyncio.gather(
            *(_bounded_fetch(bpn, did) for bpn, did in bpn_did_dict.items())
        )

    async def _run_loop(self) -> None:
        while self._task is not None:
            await self._fetch_single_round()
            await asyncio.sleep(self._poll_interval)

    async def start(self) -> None:
        """Start the collector."""
        if self._task is not None and not self._task.done():
            return
        self._task = asyncio.create_task(self._run_loop())

    async def shutdown(self) -> None:
        """Shut down the collector."""
        if self._task is not None:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
            self._task = None

    def get_catalogs(self) -> list[Any]:
        """Return the federated catalog."""
        return list(self._catalogs.values())
