from abc import ABC, abstractmethod
from typing import Any, Dict

import falcon

from api.resources import Resource


class Middleware(ABC):
    @abstractmethod
    def process_request(self, req: falcon.Request, resp: falcon.Response) -> None:
        pass

    @abstractmethod
    def process_resource(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        resource: Resource,
        params: Dict[str, Any],
    ) -> None:
        pass

    @abstractmethod
    def process_response(
        self, req: falcon.Request, resp: falcon.Response, resource: Any
    ) -> None:
        pass
