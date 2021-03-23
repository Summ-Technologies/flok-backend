import logging
from datetime import datetime
from typing import Dict, List

from flask import g
from flask_restful import Resource
from hawk_core.hawk_managers import CompanyManager, RetreatManager, UserManager
from hawk_db.retreat import RetreatItemState, RetreatToItem
from hawk_models.retreat import (
    RetreatApiModelSchema,
    RetreatEmployeeData,
    RetreatEmployeeDataSchema,
)
from pytz import timezone
from summ_web import responses
from webargs import fields
from webargs.flaskparser import use_args

from .. import app, db, jwt

logger = logging.getLogger(__name__)

company_manager = CompanyManager(db.session, app.config)
retreat_manager = RetreatManager(db.session, app.config)
user_manager = UserManager(db.session, app.config)


class RetreatController(Resource):
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
                    {"retreat": RetreatApiModelSchema.dump(obj=retreat)}
                )
        return responses.error(
            "Can't find retreat or item.", status_code=404, error_code=None
        )


class RetreatEmployeeLocationController(Resource):
    post_args = {
        "locations": fields.Nested(
            "RetreatEmployeeLocationModelSchema",
            many=True,
            required=True,
        ),
        "extra_info": fields.String(required=False),
    }

    @jwt.requires_auth
    @use_args(post_args, location="json")
    def post(self, post_args: Dict[str, any], id: int, item_id: int):
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
                retreat_items: List[RetreatToItem] = list(
                    filter(
                        lambda item: item.retreat_item.id == item_id,
                        retreat.retreat_items,
                    )
                )
                if retreat_items:
                    retreat_to_item = retreat_items[0]
                    retreat_manager.update_employee_location_saved_data(
                        retreat_to_item,
                        RetreatEmployeeData(
                            locations=post_args["locations"],
                            timestamp=datetime.now(tz=timezone("UTC")),
                            extra_info=post_args.get("extra_info"),
                        ),
                    )
                    if retreat_to_item.state == RetreatItemState.IN_PROGRESS:
                        retreat_manager.advance_retreat_items(retreat)
                    retreat_manager.commit_changes()
                    return responses.success(
                        {"retreat": RetreatApiModelSchema.dump(obj=retreat)}
                    )

        return responses.error(
            "Can't find retreat or item.", status_code=404, error_code=None
        )
