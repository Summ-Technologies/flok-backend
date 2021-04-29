from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import JSON, Numeric

from . import base


class Retreat(base.Base):
    """Retreat table"""

    __tablename__ = "retreats"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    data = Column(JSON)  # for storing misc data on retreat

    # Metadata
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc)
    )

    # Relationships
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    employee_location_submissions = relationship(
        "RetreatEmployeeLocationSubmission",
        order_by="desc(RetreatEmployeeLocationSubmission.created_at)",
    )
    proposals = relationship(
        "RetreatProposal",
        primaryjoin="Retreat.id == RetreatProposal.retreat_id",
        order_by="desc(RetreatProposal.created_at)",
    )
    flok_note = Column(String)
    selected_proposal_id = Column(Integer, ForeignKey("retreats_proposals.id"))
    num_employees = Column(Integer, default=10, nullable=False)
    num_nights = Column(Integer, default=4, nullable=False)


class RetreatEmployeeLocationSubmission(base.Base):

    __tablename__ = "retreats_employees_locations_submissions"

    id = Column(Integer, primary_key=True)
    retreat_id = Column(Integer, ForeignKey("retreats.id"))

    extra_info = Column(String)  # extra info with the submission

    location_items = relationship("RetreatEmployeeLocationItem", lazy="joined")

    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc)
    )


class RetreatEmployeeLocationItem(base.Base):

    __tablename__ = "retreats_employees_locations_items"

    id = Column(Integer, primary_key=True)
    submission_id = Column(
        Integer,
        ForeignKey("retreats_employees_locations_submissions.id"),
        nullable=False,
    )

    employee_count = Column(Integer, nullable=False)

    google_place_id = Column(String, nullable=False)
    main_text = Column(String, nullable=False)
    secondary_text = Column(String, nullable=False)


class RetreatProposal(base.Base):

    __tablename__ = "retreats_proposals"

    id = Column(Integer, primary_key=True)
    retreat_id = Column(Integer, ForeignKey("retreats.id"))

    image_url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    body = Column(String)

    flight_time_avg = Column(Numeric(4, 2), nullable=False)
    flights_cost = Column(Integer, nullable=False)  # per person
    lodging_cost = Column(Integer, nullable=False)  # per night per person
    other_cost = Column(Integer, nullable=False)  # per night per person

    extra_info = Column(String)

    # Metadata
    name = Column(String)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(tz=timezone.utc),
        nullable=False,
    )
