from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import JSON
from sqlalchemy.sql.sqltypes import Enum as pgEnum

from . import base


class Retreat(base.Base):
    """Retreat table"""

    __tablename__ = "retreats"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=True)
    data = Column(JSON, nullable=True)  # for storing misc data on retreat

    # Metadata
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc)
    )

    # Relationships
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    retreat_items = relationship(
        "RetreatToItem",
        order_by="RetreatToItem.order",
        collection_class=ordering_list("order"),
    )


class RetreatItemType(Enum):
    INTAKE_CALL = "INTAKE_CALL"
    EMPLOYEE_LOCATIONS = "EMPLOYEE_LOCATIONS"
    INITIAL_PROPOSALS = "INITIAL_PROPOSALS"
    DESTINATION_SELECTION = "DESTINATION_SELECTION"
    POST_PAYMENT = "POST_PAYMENT"


class RetreatItem(base.Base):
    """Retreat item table"""

    __tablename__ = "retreats_items"

    id = Column(Integer, primary_key=True)
    type = Column(pgEnum(RetreatItemType), nullable=False)
    data = Column(JSON, nullable=False)
    title = Column(String, nullable=False)
    subtitle = Column(String)


class RetreatItemState(Enum):
    TODO = "TODO"
    DONE = "DONE"
    IN_PROGRESS = "IN_PROGRESS"


class RetreatToItem(base.Base):
    """
    Retreat to retreat items table
    Also contains order and current state information.
    """

    __tablename__ = "retreats_to_items"

    # Relationship
    retreat_id = Column(Integer, ForeignKey("retreats.id"), primary_key=True)
    retreat_item_id = Column(Integer, ForeignKey("retreats_items.id"), primary_key=True)

    retreat_item = relationship("RetreatItem", lazy="joined")

    order = Column(Integer, nullable=False)
    state = Column(pgEnum(RetreatItemState), nullable=False)
    data = Column(JSON)  # overrides retreat item data
    saved_data = Column(JSON)  # overrides retreat item data
