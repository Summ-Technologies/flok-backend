from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import JSON, Boolean
from sqlalchemy.sql.sqltypes import Enum as pgEnum

from . import base


class RetreatCheckoutOrder(base.Base):
    """Associates checkout order with a retreat"""

    __tablename__ = "retreats_checkout_orders"

    retreat_id = Column(Integer, ForeignKey("retreats.id"), primary_key=True)
    order_id = Column(Integer, ForeignKey("checkout_orders.id"), primary_key=True)


class CheckoutOrder(base.Base):
    """CheckoutOrder models order submitted and payment info"""

    __tablename__ = "checkout_orders"

    id = Column(Integer, primary_key=True)
    checkout_session_id = Column(String, nullable=False, unique=True)
    customer_id = Column(String, ForeignKey("stripe_customers.customer_id"))
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
