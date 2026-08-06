from local_fc.routers.agreements import agreements_router
from local_fc.routers.catalogs import catalogs_router
from local_fc.routers.health import health_router
from local_fc.routers.negotiations import negotiations_router
from local_fc.routers.partners import partners_router
from local_fc.routers.trigger import trigger_router

routers = [
    agreements_router,
    catalogs_router,
    health_router,
    negotiations_router,
    partners_router,
    trigger_router,
]

__all__ = ["routers"]
