import logging

import stripe
from flask import request
from flask_restful import Resource
from robin_core.robin_managers import RobinManager
from summ_web import responses

from .. import app, db

logger = logging.getLogger(__name__)

robin_manager = RobinManager(db.session, app.config)


class WebhookController(Resource):
    def post(self):
        payload = request.get_data()
        sig_header = request.headers.get("STRIPE_SIGNATURE")
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, app.config["STRIPE_WEBHOOK_SECRET"]
            )
        except ValueError as e:
            return responses.error(
                error_message="Invalid payload", error_code=None, status_code=400
            )
        except stripe.error.SignatureVerificationError as e:
            return responses.error(
                error_message="Invalid signature", error_code=None, status_code=400
            )

        event_dict = event.to_dict()
        intent = event_dict["data"]["object"]
        stripe_payment = robin_manager.get_stripe_payment(intent["id"])
        if stripe_payment:
            stripe_payment.currency = intent["currency"]
            stripe_payment.client_secret = intent["client_secret"]
            stripe_payment.customer_id = intent["customer"]
            stripe_payment.status = intent["status"].lstrip("payment_intent.").upper()
            stripe_payment.amount = intent["amount"]
            robin_manager.session.add(stripe_payment)
            robin_manager.commit_changes()

        return responses.success("OK")
