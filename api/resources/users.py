import falcon
from marshmallow import Schema, fields

from api.resources import Resource
from core.commands.registration import RegisterCommand
from core.commands.user_data import GetUsersDataCommand
from core.commands.whoami import WhoAmICommand


class WhoAmISchema(Schema):
    is_admin = fields.Bool(dump_only=True)


class WhoAmIResource(Resource):
    schema: Schema = WhoAmISchema()
    check_maintenance_mode = False

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        resp.payload = WhoAmICommand().handle()
        resp.status = falcon.HTTP_200


class RegistrationSchema(Schema):
    email = fields.Email(required=True, load_only=True)
    password = fields.Str(required=True, load_only=True)


class RegistrationResource(Resource):
    schema: Schema = RegistrationSchema()

    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        RegisterCommand(**req.payload).handle()
        resp.status = falcon.HTTP_201


class UsersInternalResourceSchema(Schema):
    emails = fields.List(fields.Email, dump_only=True)


class UsersInternalResource(Resource):
    schema: Schema = UsersInternalResourceSchema()
    check_maintenance_mode = False

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        resp.payload = GetUsersDataCommand().handle()
        resp.status = falcon.HTTP_200
