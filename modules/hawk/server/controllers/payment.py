import logging
from typing import Dict, List

from flask import g
from flask_restful import Resource
from hawk_core.hawk_managers import RetreatManager
from hawk_db.retreat import RetreatProposal
from robin_core.robin_managers import RobinManager
from summ_web import responses
from webargs import fields
from webargs.flaskparser import use_args

from .. import app, db, jwt

logger = logging.getLogger(__name__)

robin_manager: RobinManager = RobinManager(db.session, app.config)
retreat_manager: RetreatManager = RetreatManager(db.session, app.config)


class CheckoutRetreatController(Resource):
    post_args = {
        "proposal_id": fields.Int(requred=True),
        "retreat_id": fields.Int(required=True),
        "redirect_url": fields.Url(required=True),
    }

    @jwt.requires_auth
    @use_args(post_args, location="json")
    def post(self, post_args: Dict[str, any]):
        flok_fee = 12500  # $125
        retreat = retreat_manager.get_retreat(post_args["retreat_id"], g.user)
        if retreat:
            matches: List[RetreatProposal] = list(
                filter(lambda p: p.id == post_args["proposal_id"], retreat.proposals)
            )
            if matches:
                proposal = matches[0]
                stripe_customer = robin_manager.get_stripe_customer(g.user)
                if not stripe_customer:
                    stripe_customer = robin_manager.create_stripe_customer(g.user)
                stripe_checkout_session = robin_manager.create_stripe_checkout_session(
                    customer=stripe_customer,
                    image=proposal.image_url,
                    name="Flok fee (per employee)",
                    price=flok_fee,
                    quantity=retreat.num_employees,
                    success_url=post_args["redirect_url"],
                    cancel_url=post_args["redirect_url"],
                    metadata={
                        "retreat_id": retreat.id,
                        "proposal_id": proposal.id,
                    },
                )
                robin_manager.commit_changes()
                return responses.success({"session_id": stripe_checkout_session.id})
