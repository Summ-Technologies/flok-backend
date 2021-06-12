import logging

from flask import g
from flask_restful import Resource
from hawk_core.hawk_managers import CompanyManager, UserManager
from hawk_models.company import CompanyApiSchema
from hawk_models.user import UserApiSchema
from summ_web import responses

from .. import app, db, jwt

logger = logging.getLogger(__name__)

company_manager = CompanyManager(db.session, app.config)
user_manager = UserManager(db.session, app.config)


class UserHomeController(Resource):
    @jwt.requires_auth
    def get(self):
        """Get's user and company info on current logged in user.

        Returns JSON
          user: UserApiSchema
          company?: CompanyApiSchema
        """
        response = {"user": UserApiSchema.dump(obj=g.user)}

        companies = company_manager.get_companies(g.user, is_admin=True)

        if companies:
            company = companies[0]
            response.update({"company": CompanyApiSchema.dump(obj=company)})

        return responses.success(response)
