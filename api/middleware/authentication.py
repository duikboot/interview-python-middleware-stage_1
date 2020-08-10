import re
from typing import Any, Dict

import falcon
from haps import Inject

import settings
from api.middleware import Middleware
from api.resources import Resource
from core.registry import Registry

API_KEY_REGEX = re.compile(r".*user-session.*Apikey\s+(?P<token>\b\w+\b)")


def is_correct_api_key(access_token: str) -> bool:
    """
    >>> is_correct_api_key("Bearer user-session")
    False
    >>> is_correct_api_key("Bearer user-session,")
    False
    >>> is_correct_api_key(" Bearer user-session")
    False
    >>> is_correct_api_key("Bearer user-session,Apikey ILoveKittens")
    True
    >>> is_correct_api_key("Bearer user-session, Apikey ILoveKittens ")
    True
    >>> is_correct_api_key("Bearer user-session, Apikey ILoveKittens,")
    True
    >>> is_correct_api_key("Bearer user-session, Apikey ILoveKittens")
    True
    """

    match = API_KEY_REGEX.match(access_token)

    if match:
        token = match.group("token")

        if token == settings.API_KEY:
            return True

    return False


class AuthenticationMiddleware(Middleware):
    registry: Registry = Inject()

    def process_request(self, req: falcon.Request, resp: falcon.Response) -> None:
        token = req.auth
        relative_uri = req.relative_uri

        if not token:
            if relative_uri not in settings.NO_AUTH_REQUIRED.uris:
                if relative_uri in settings.NO_SESSION_TOKEN_REQUIRED.uris:
                    raise falcon.HTTPUnauthorized("Unauthorized")
                raise falcon.HTTPForbidden("Forbidden")

        if token:

            token_type, _, access_token = token.partition(" ")
            if token_type != "Bearer":
                falcon.HTTPForbidden("Forbidden")

            if is_correct_api_key(access_token):
                level = 3
            elif not access_token:
                level = 1
            else:
                level = 2

            auth_type = next(i for i in settings.AUTH_CLASSES
                             if relative_uri in i.uris)

            auth = auth_type.__class__(auth_type.uris, level)

            if auth < auth_type:
                if level == 1:
                    raise falcon.HTTPUnauthorized("Unauthorized")
                raise falcon.HTTPForbidden("Forbidden")

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
