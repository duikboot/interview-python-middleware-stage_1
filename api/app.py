from typing import Dict

import falcon
from haps import Container

from api.middleware.authentication import AuthenticationMiddleware
from api.middleware.maintenance_mode import MaintenanceModeMiddleware
from api.middleware.marshmallow import MarshmallowMiddleware
from api.middleware.registry import RegistryMiddleware
from api.resources.collections import CollectionsInternalResource, CollectionsResource
from api.resources.users import (
    RegistrationResource,
    UsersInternalResource,
    WhoAmIResource,
)
from core.exceptions import NotAuthenticatedError

middleware = [
    RegistryMiddleware(),
    MaintenanceModeMiddleware(),
    AuthenticationMiddleware(),
    MarshmallowMiddleware(),
]


routes = [
    ("/auth/register", RegistrationResource),
    ("/users/whoami", WhoAmIResource),
    ("/collections", CollectionsResource),
    ("/internal/users", UsersInternalResource),
    ("/internal/collections", CollectionsInternalResource),
]

# configure dependency injection
Container.autodiscover(["core"])


app = falcon.API(middleware=middleware)

for route, resource in routes:
    app.add_route(route, resource())


def handle_authentication_error(
    exception: Exception,
    request: falcon.Request,
    response: falcon.Response,
    params: Dict,
) -> None:
    raise falcon.HTTPUnauthorized()


app.add_error_handler(NotAuthenticatedError, handle_authentication_error)
