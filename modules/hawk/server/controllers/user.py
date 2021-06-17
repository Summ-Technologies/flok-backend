import logging

from flask import g
from flask_restful import Resource
from hawk_core.hawk_managers import CompanyManager, RetreatManager, UserManager
from hawk_models.company import CompanySchema
from hawk_models.user import UserSchema
from summ_web import responses

from .. import app, db, jwt

logger = logging.getLogger(__name__)

company_manager = CompanyManager(db.session, app.config)
user_manager = UserManager(db.session, app.config)
retreat_manager = RetreatManager(db.session, app.config)


class UserHomeController(Resource):
    @jwt.requires_auth
    def get(self):
        """Get's user info on current logged in user.

        Returns JSON
          user: UserSchema
          company: CompanySchema
          retreat: RetreatSchema
        """
        ret = {"user": UserSchema().dump(obj=g.user)}
        company = company_manager.get_company(g.user)
        if company:
            ret.update({"company": CompanySchema().dump(obj=company)})
        return responses.success(ret)
