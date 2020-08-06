from typing import Any, Dict

import falcon

import settings
from api.middleware import Middleware
from api.resources import Resource


class MaintenanceModeMiddleware(Middleware):
    def process_request(self, req: falcon.Request, resp: falcon.Response) -> None:
        pass

    def process_resource(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        resource: Resource,
        params: Dict[str, Any],
    ) -> None:
        if resource.check_maintenance_mode is True:
            if settings.MAINTENANCE_MODE is True:
                raise falcon.HTTPServiceUnavailable(
                    "Maintenance Mode", "Service is in maintenance mode"
                )

    def process_response(
        self, req: falcon.Request, resp: falcon.Response, resource: Resource
    ) -> None:
        pass
