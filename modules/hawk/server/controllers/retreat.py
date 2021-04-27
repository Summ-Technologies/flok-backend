import logging
from typing import Dict

from flask import g
from flask_restful import Resource
from hawk_core.hawk_managers import CompanyManager, RetreatManager, UserManager
from hawk_models.retreat import RetreatApiSchema, RetreatProposalApiSchema
from summ_web import responses
from webargs import fields
from webargs.flaskparser import use_args

from .. import app, db, jwt

logger = logging.getLogger(__name__)

company_manager = CompanyManager(db.session, app.config)
retreat_manager = RetreatManager(db.session, app.config)
user_manager = UserManager(db.session, app.config)

class RetreatProposalsController(Resource):
    @jwt.requires_auth
    def get(self, id: int):
        companies = company_manager.get_companies(g.user, is_admin=True)
        if companies:
            company = companies[0]
            retreats = list(
                filter(
                    lambda _retreat: _retreat.id == id,
                    retreat_manager.get_retreats(company),
                )
            )
            if retreats:
                retreat = retreats[0]
                return responses.success(
                    {
                        "proposals": RetreatProposalApiSchema.dump(
                            obj=retreat.proposals, many=True
                        )
                    }
                )
        return responses.error("Can't find retreat.", status_code=404, error_code=None)


class RetreatEmployeeLocationV2Controller(Resource):
    post_args = {"submission": fields.Nested("RetreatEmployeeLocationSubmissionSchema")}

    @jwt.requires_auth
    @use_args(post_args, location="json")
    def post(self, post_args: Dict[str, any], id: int):
        companies = company_manager.get_companies(g.user, is_admin=True)
        if companies:
            company = companies[0]
            retreats = list(
                filter(
                    lambda _retreat: _retreat.id == id,
                    retreat_manager.get_retreats(company),
                )
            )
            if retreats:
                retreat = retreats[0]
                retreat_manager.add_employee_location_submission(
                    retreat, post_args["submission"]
                )
                retreat_manager.commit_changes()
                return responses.success(
                    {
                        "retreat": RetreatApiSchema.dump(obj=retreat),
                    }
                )

        return responses.error("Can't find retreat.", status_code=404, error_code=None)
