import logging
from typing import List, Optional

import stripe
from hawk_db.payment import CheckoutOrder, RetreatCheckoutOrder, StripeCustomer
from hawk_db.user import User
from sqlalchemy.sql.schema import MetaData

from .base_manager import BaseManager

logger = logging.getLogger(__name__)


class RobinManager(BaseManager):
    def validate_config(self, config: dict):
        """
        Required config values:
            STRIPE_API_KEY, CLIENT_BASE_URL
        """
        stripe_api_key = config.get("STRIPE_API_KEY")
        assert stripe_api_key is not None, "Missing STRIPE_API_KEY config"
        stripe.api_key = stripe_api_key
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

    def create_checkout_order(
        self,
        customer_id: str,
        session_id: str,
        amount: int,
        currency: str,
        metadata: dict,
    ):
        checkout = CheckoutOrder()
        checkout.amount = amount
        checkout.customer_id = customer_id
        checkout.checkout_session_id = session_id
        checkout.currency = currency
        self.session.add(checkout)
        self.session.flush()
        if metadata and metadata.get("retreat_id"):
            retreat_checkout = RetreatCheckoutOrder()
            retreat_checkout.order_id = checkout.id
            retreat_checkout.retreat_id = metadata.get("retreat_id")
            self.session.add(retreat_checkout)
            self.session.flush()
        return checkout

    def create_stripe_checkout_session(
        self,
        customer: StripeCustomer,
        name: str,
        image: str,
        price: int,
        quantity: int,
        cancel_url: str,
        success_url: str,
        metadata: Optional[dict] = None,
    ):
        return stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer=customer.customer_id,
            metadata=metadata,
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": price,
                        "product_data": {
                            "name": name,
                            "images": [image],
                        },
                    },
                    "quantity": quantity,
                },
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )
