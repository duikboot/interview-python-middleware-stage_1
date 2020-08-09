from dataclasses import dataclass

MAINTENANCE_MODE = False
API_KEY = "ILoveKittens"


@dataclass(order=True)
class AuthOrder:
    uris: tuple
    order: int


NO_AUTH_REQUIRED = AuthOrder(("/auth/register", "/collections"), 1)

NO_SESSION_TOKEN_REQUIRED = AuthOrder(("/users/whoami",), 2)

SESSION_TOKEN_REQUIRED = AuthOrder(
    ("/internal/users", "/internal/collections"), 3)

AUTH_CLASSES = (NO_AUTH_REQUIRED, NO_SESSION_TOKEN_REQUIRED,
                SESSION_TOKEN_REQUIRED)
