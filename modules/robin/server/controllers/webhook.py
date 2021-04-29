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
        if event_dict["type"] == "checkout.session.completed":
            session = event_dict["data"]["object"]
            if session["payment_status"] == "paid":
                checkout_order = robin_manager.create_checkout_order(
                    session_id=session["id"],
                    customer_id=session["customer"],
                    amount=session["amount_total"],
                    currency=session["currency"],
                    metadata=session["metadata"],
                )
                if checkout_order:
                    robin_manager.commit_changes()
                    return responses.success("OK")
        return responses.error("Not found", status_code=404, error_code=None)
