from typing import Any, Dict

import falcon
from haps import Inject

from api.middleware import Middleware
from api.resources import Resource
from core.registry import Registry


class RegistryMiddleware(Middleware):
    registry: Registry = Inject()

    def process_request(self, req: falcon.Request, resp: falcon.Response) -> None:
        self.registry.initialize()

    def process_resource(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        resource: Resource,
        params: Dict[str, Any],
    ) -> None:
        pass  # do nothing

    def process_response(
        self, req: falcon.Request, resp: falcon.Response, resource: Resource
    ) -> None:
        self.registry.clean()
