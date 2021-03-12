import logging

from flask import g
from flask_restful import Resource
from hawk_models.user import UserApiModelSchema
from summ_web import responses

from .. import jwt

logger = logging.getLogger(__name__)


class UserHomeController(Resource):
    @jwt.requires_auth
    def get(self):
        return responses.success({"user": UserApiModelSchema.dump(obj=g.user)})
