from local_fc.routers.catalogs import catalogs_router
from local_fc.routers.health import health_router
from local_fc.routers.partners import partners_router
from local_fc.routers.trigger import trigger_router

routers = [catalogs_router, health_router, partners_router, trigger_router]

__all__ = ["routers"]
