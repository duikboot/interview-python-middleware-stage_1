import json
from typing import Any, Dict, Optional, cast

import falcon
from marshmallow import Schema, ValidationError, utils

from api.middleware import Middleware
from api.resources import Resource


class MarshmallowMiddleware(Middleware):
    SAFE_METHODS = ("get", "options", "head")

    def process_request(self, req: falcon.Request, resp: falcon.Response) -> None:
        req.payload = {}
        is_json_request = req.content_type and req.content_type.startswith(
            "application/json"
        )

        if not (req.content_length and is_json_request):
            return

        req.raw_body = req.stream.read(req.content_length)

        try:
            req.payload = json.loads(req.raw_body)
            assert isinstance(req.payload, dict)
        except (json.JSONDecodeError, AssertionError):
            raise falcon.HTTPBadRequest("Invalid body format", "Body is not a valid JSON")

    def process_resource(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        resource: Resource,
        params: Dict[str, Any],
    ) -> None:
        method = req.method.lower()
        schema = self._get_schema(resource, method, "request")

        if (
            method == "options"
            or not schema
            or (method in self.SAFE_METHODS and not resource.force_use_schema)
        ):
            return

        data = req.payload.copy()
        data.update(req.params)

        try:
            result = schema.load(data)
        except ValidationError as err:
            # @validates_schema returns errors under the "_schema" key
            err_messages = (
                cast(Dict[str, str], err.messages).get("_schema") or err.messages
            )
            raise falcon.HTTPBadRequest("Validation Error", err_messages)

        req.payload = result

        for param in params:
            if param in result:
                params[param] = result[param]

    def process_response(
        self, req: falcon.Request, resp: falcon.Response, resource: Resource
    ) -> None:
        try:
            payload = resp.payload
        except AttributeError:
            pass
        else:
            method = req.method.lower()
            schema = self._get_schema(resource, method, "response")

            if not schema and bool(payload):
                resp.body = json.dumps(payload)

            if not schema:
                return

            try:
                data = schema.dumps(payload, many=utils.is_collection(payload))
            except ValidationError as err:
                raise falcon.HTTPInternalServerError(
                    title="Could not serialize response",
                    description=json.dumps(err.messages),
                )

            resp.body = data

    @classmethod
    def _get_schema(
        cls, resource: Resource, method: str, msg_type: str
    ) -> Optional[Schema]:
        """
        Returns specific schema, generic schema or None.
        """
        schema = cls._get_specific_schema(resource, method, msg_type)

        if schema is None:
            schema = getattr(resource, "schema", None)

        if schema and not isinstance(schema, Schema):
            raise TypeError("Schema for resource must be Marshmallow schema.")

        return schema

    @staticmethod
    def _get_specific_schema(
        resource: Resource, method: str, msg_type: str
    ) -> Optional[Schema]:
        sch_name = f"{method.lower()}_{msg_type}_schema"
        specific_schema: Optional[Schema] = getattr(resource, sch_name, None)
        if specific_schema is not None:
            return specific_schema

        sch_name = f"{method.lower()}_schema"
        specific_schema = getattr(resource, sch_name, None)
        return specific_schema
