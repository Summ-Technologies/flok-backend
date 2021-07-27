import logging

from flask import g
from flask_restful import Resource
from hawk_core.hawk_managers import UserManager
from hawk_models.user import UserSchema
from summ_web import responses

from .. import app, db, jwt

logger = logging.getLogger(__name__)

user_manager = UserManager(db.session, app.config)


class UserHomeController(Resource):
    @jwt.requires_auth
    def get(self):
        """Get's user info on current logged in user.

        Returns JSON
          user: UserSchema
        """
        ret = {"user": UserSchema().dump(obj=g.user)}
        return responses.success(ret)
