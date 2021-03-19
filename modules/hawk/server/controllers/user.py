import logging

from flask import g
from flask_restful import Resource
from hawk_core.hawk_managers import CompanyManager, RetreatManager, UserManager
from hawk_db.company import CompanyAdmin
from hawk_db.retreat import Retreat
from hawk_models.company import CompanyApiModelSchema
from hawk_models.retreat import RetreatApiModelSchema
from hawk_models.user import UserApiModelSchema
from summ_web import responses

from .. import app, db, jwt

logger = logging.getLogger(__name__)

company_manager = CompanyManager(db.session, app.config)
retreat_manager = RetreatManager(db.session, app.config)
user_manager = UserManager(db.session, app.config)


class UserHomeController(Resource):
    @jwt.requires_auth
    def get(self):
        response = {"user": UserApiModelSchema.dump(obj=g.user)}

        companies = company_manager.get_companies(g.user, is_admin=True)

        if companies:
            company = companies[0]
            response.update({"company": CompanyApiModelSchema.dump(obj=company)})

            retreats = retreat_manager.get_retreats(company)
            if retreats:
                retreat = retreats[0]
                response.update({"retreat": RetreatApiModelSchema.dump(obj=retreat)})

        return responses.success(response)
