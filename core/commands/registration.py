from core.commands import Command


class RegisterCommand(Command):
    email: str
    password: str

    def handle(self) -> None:
        assert self.email
        assert self.password
