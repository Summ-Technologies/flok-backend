import logging

from flask import g
from flask_restful import Resource
from robin_core.robin_managers import RobinManager
from summ_web import responses

from .. import app, db, jwt

logger = logging.getLogger(__name__)

robin_manager: RobinManager = RobinManager(db.session, app.config)


class PaymentController(Resource):
    @jwt.requires_auth
    def post(self):
        stripe_customer = robin_manager.get_stripe_customer(g.user)
        if not stripe_customer:
            stripe_customer = robin_manager.create_stripe_customer(g.user)
        stripe_payment_intent = robin_manager.create_stripe_payment(
            stripe_customer, amount=100
        )
        robin_manager.commit_changes()
        return responses.success({"client_secret": stripe_payment_intent.client_secret})
