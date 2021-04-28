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


class RetreatFilterDetailsController(Resource):
    """This controller edits numEmployees and numNights retreat filter details"""

    put_args = {
        "num_employees": fields.Integer(required=True),
        "num_nights": fields.Integer(required=False),
    }

    @jwt.requires_auth
    @use_args(put_args, location="json")
    def put(self, put_args: Dict[str, int], retreat_id: int):
        retreat = retreat_manager.get_retreat(retreat_id, g.user)
        if retreat:
            retreat_manager.update_retreat_filter_details(
                retreat, put_args["num_employees"], put_args.get("num_nights")
            )
            retreat_manager.commit_changes()
            return responses.success({"retreat": RetreatApiSchema.dump(obj=retreat)})
        return responses.error("Can't find retreat", status_code=404, error_code=None)


class RetreatProposalSelectedController(Resource):
    """This controller adds (or removes) selected proposals"""

    post_args = {"proposal_id": fields.Integer(required=True)}

    @jwt.requires_auth
    @use_args(post_args, location="json")
    def post(self, post_args: Dict[str, int], retreat_id: int):
        """Select prefered retreat proposal"""
        retreat = retreat_manager.get_retreat(retreat_id, g.user)
        if retreat:
            if retreat_manager.select_retreat_proposal(
                retreat, post_args["proposal_id"]
            ):
                retreat_manager.commit_changes()
                return responses.success(
                    {"retreat": RetreatApiSchema.dump(obj=retreat)}
                )
            else:
                return responses.error(
                    "Can't find proposal", status_code=404, error_code=None
                )
        else:
            return responses.error(
                "Can't find retreat", status_code=404, error_code=None
            )

    @jwt.requires_auth
    def delete(self, retreat_id: int):
        """Unselect prefered retreat proposal"""
        retreat = retreat_manager.get_retreat(retreat_id, g.user)
        if retreat:
            retreat_manager.unselect_retreat_proposal(retreat)
            retreat_manager.commit_changes()
            return responses.success({"retreat": RetreatApiSchema.dump(obj=retreat)})
        else:
            return responses.error(
                "Can't find retreat", status_code=404, error_code=None
            )


class RetreatEmployeeLocationV2Controller(Resource):
    post_args = {"submission": fields.Nested("RetreatEmployeeLocationSubmissionSchema")}

    @jwt.requires_auth
    @use_args(post_args, location="json")
    def post(self, post_args: Dict[str, any], retreat_id: int):
        companies = company_manager.get_companies(g.user, is_admin=True)
        if companies:
            company = companies[0]
            retreats = list(
                filter(
                    lambda _retreat: _retreat.id == retreat_id,
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
