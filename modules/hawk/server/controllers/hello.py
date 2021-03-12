import logging

from flask import g
from flask_restful import Resource
from summ_web import responses

from .. import jwt

logger = logging.getLogger(__name__)


class HelloController(Resource):
    def get(self):
        return responses.success({"message": "Hello world!"})


class HelloSecuredController(Resource):
    @jwt.requires_auth
    def get(self):
        return responses.success({"message": f"Hello {g.user} secured world!"})
