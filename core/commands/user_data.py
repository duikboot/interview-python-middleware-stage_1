from typing import Dict, List

from core.commands import Command


class GetUsersDataCommand(Command):
    def handle(self) -> Dict[str, List[str]]:
        return {"emails": ["email1", "email2"]}
