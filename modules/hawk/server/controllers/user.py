import logging

from flask import g
from flask_restful import Resource
from hawk_db.company import CompanyAdmin
from hawk_db.retreat import Retreat
from hawk_models.company import CompanyApiModelSchema
from hawk_models.retreat import RetreatApiModelSchema
from hawk_models.user import UserApiModelSchema
from summ_web import responses

from .. import db, jwt

logger = logging.getLogger(__name__)


class UserHomeController(Resource):
    @jwt.requires_auth
    def get(self):
        response = {"user": UserApiModelSchema.dump(obj=g.user)}

        company_admin = (
            db.session.query(CompanyAdmin)
            .filter(CompanyAdmin.admin_id == g.user.id)
            .first()
        )

        if company_admin:
            response.update(
                {"company": CompanyApiModelSchema.dump(obj=company_admin.company)}
            )

            retreat = (
                db.session.query(Retreat)
                .filter(Retreat.company_id == company_admin.company_id)
                .first()
            )

            if retreat:
                print(retreat.retreat_items)
                response.update({"retreat": RetreatApiModelSchema.dump(obj=retreat)})

        return responses.success(response)
