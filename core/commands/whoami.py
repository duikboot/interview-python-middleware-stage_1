from typing import Dict

from haps import Inject

from core.commands import Command
from core.exceptions import NotAuthenticatedError
from core.registry import Registry


class WhoAmICommand(Command):
    registry: Registry = Inject()

    def handle(self) -> Dict[str, bool]:
        try:
            if self.registry.access_token is None:
                raise NotAuthenticatedError
        except AttributeError:
            raise NotAuthenticatedError

        return {"is_admin": False}
