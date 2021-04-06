import enum
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Enum as pgEnum

from . import base


class RetreatCheckoutOrder(base.Base):
    """Associates checkout order with a reatreat"""

    __tablename__ = "retreats_checkout_orders"

    retreat_id = Column(Integer, ForeignKey("retreats.id"), primary_key=True)
    order_id = Column(Integer, ForeignKey("checkout_orders.id"), primary_key=True)


class CheckoutOrder(base.Base):
    """CheckoutOrder models order submitted and payment info"""

    __tablename__ = "checkout_orders"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    payment_intent_id = Column(
        String, ForeignKey("stripe_payment_intents.id"), nullable=False
    )
    amount = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)


class StripeCustomer(base.Base):
    """Stripe customer table"""

    __tablename__ = "stripe_customers"

    customer_id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    # Metadata
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc)
    )


class StripePaymentIntentStatus(enum.Enum):
    REQUIRES_PAYMENT_METHOD = "requires_payment_method"
    REQUIRES_CONFIRMATION = "requires_confirmation"
    REQUIRES_ACTION = "requires_action"
    SUCCEEDED = "succeeded"
    CANCELED = "canceled"


class StripePaymentIntent(base.Base):
    __tablename__ = "stripe_payment_intents"

    id = Column(String, primary_key=True)
    customer_id = Column(
        String, ForeignKey("stripe_customers.customer_id"), nullable=False
    )
    client_secret = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)
    status = Column(pgEnum(StripePaymentIntentStatus), nullable=False)
