from typing import Any, Dict

import falcon
from haps import Inject

from api.middleware import Middleware
from api.resources import Resource
from core.registry import Registry


class AuthenticationMiddleware(Middleware):
    registry: Registry = Inject()

    def process_request(self, req: falcon.Request, resp: falcon.Response) -> None:
        token = req.auth
        if not token:
            return
        token_type, _, access_token = token.partition(" ")
        if token_type == "Bearer":
            self.registry.access_token = access_token  # type: ignore

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
        pass
