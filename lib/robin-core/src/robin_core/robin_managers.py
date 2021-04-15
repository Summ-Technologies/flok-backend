import logging
from typing import List, Optional

import stripe
from hawk_db.payment import StripeCustomer
from hawk_db.user import User

from .base_manager import BaseManager

logger = logging.getLogger(__name__)


class RobinManager(BaseManager):
    def validate_config(self, config: dict):
        """
        Required config values:
            STRIPE_API_KEY, STRIPE_WEBHOOK_SECRET, CLIENT_BASE_URL
        """
        stripe_api_key = config.get("STRIPE_API_KEY")
        assert stripe_api_key is not None, "Missing STRIPE_API_KEY config"
        stripe.api_key = stripe_api_key
        assert (
            config.get("STRIPE_WEBHOOK_SECRET") is not None
        ), "Missing STRIPE_WEBHOOK_SECRET config"
        assert (
            config.get("CLIENT_BASE_URL") is not None
        ), "Missing CLIENT_BASE_URL config"

    def create_stripe_customer(self, user: User) -> StripeCustomer:
        customer = stripe.Customer.create(email=user.email, metadata={"id": user.id})
        if customer:
            new_stripe_customer = StripeCustomer()
            new_stripe_customer.customer_id = customer.id
            new_stripe_customer.user_id = user.id
            self.session.add(new_stripe_customer)
            self.session.flush()
            return new_stripe_customer

    def get_stripe_customer(self, user: User) -> Optional[StripeCustomer]:
        return (
            self.session.query(StripeCustomer)
            .filter(StripeCustomer.user_id == user.id)
            .one_or_none()
        )

    def create_stripe_checkout_session(self, customer: StripeCustomer):
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer=customer.customer_id,
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": 2000,
                        "product_data": {
                            "name": "Stubborn Attachments",
                            "images": ["https://i.imgur.com/EHyR2nP.png"],
                        },
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=self.config["CLIENT_BASE_URL"] + "?success=true",
            cancel_url=self.config["CLIENT_BASE_URL"] + "?canceled=true",
        )
        pass

    def create_stripe_checkout_session():
        pass
