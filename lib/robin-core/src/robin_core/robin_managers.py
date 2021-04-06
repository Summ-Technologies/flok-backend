import logging
from typing import List, Optional

import stripe
from hawk_db.payment import StripeCustomer, StripePaymentIntent
from hawk_db.user import User

from .base_manager import BaseManager

logger = logging.getLogger(__name__)


class RobinManager(BaseManager):
    def validate_config(self, config: dict):
        stripe_api_key = config.get("STRIPE_API_KEY")
        assert stripe_api_key is not None, "Missing STRIPE_API_KEY config"
        stripe.api_key = stripe_api_key
        assert (
            config.get("STRIPE_WEBHOOK_SECRET") is not None
        ), "Missing STRIPE_WEBHOOK_SECRET config"

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

    def create_stripe_payment(
        self, customer: StripeCustomer, amount: int, currency: str = "usd"
    ) -> StripePaymentIntent:
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"],
            customer=customer.customer_id,
        )
        if payment_intent:
            new_stripe_payment = StripePaymentIntent()
            new_stripe_payment.amount = payment_intent.amount
            new_stripe_payment.client_secret = payment_intent.client_secret
            new_stripe_payment.currency = payment_intent.currency
            new_stripe_payment.customer_id = customer.customer_id
            new_stripe_payment.status = payment_intent.status.upper()
            new_stripe_payment.id = payment_intent.id
            self.session.add(new_stripe_payment)
            self.session.flush()
            return new_stripe_payment

    def get_stripe_payments(
        self, customer: StripeCustomer
    ) -> List[StripePaymentIntent]:
        return (
            self.session.query(StripePaymentIntent)
            .filter(StripePaymentIntent.customer_id == customer.customer_id)
            .all()
        )

    def get_stripe_payment(self, payment_id: str) -> Optional[StripePaymentIntent]:
        return self.session.query(StripePaymentIntent).get(payment_id)
