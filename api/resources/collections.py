import falcon
from marshmallow import Schema, fields

from api.resources import Resource
from core.commands.collections import GetCollectionsCommand, GetCollectionsInternalCommand


class CollectionsSchema(Schema):
    collections = fields.List(fields.String, dump_only=True)


class CollectionsResource(Resource):
    schema: Schema = CollectionsSchema()

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        resp.payload = GetCollectionsCommand().handle()
        resp.status = falcon.HTTP_200


class CollectionsInternalResource(Resource):
    check_maintenance_mode = False
    schema: Schema = CollectionsSchema()

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        resp.payload = GetCollectionsInternalCommand().handle()
        resp.status = falcon.HTTP_200
