from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import CheckConstraint
from sqlalchemy.sql.sqltypes import Boolean, Date

from . import base


class LodgingProposalRequest(base.Base):
    """Lodging RFP table"""

    __tablename__ = "lodging_proposal_requests"
    __table_args__ = (
        CheckConstraint(
            "(NOT flexible_dates) OR (flexible_dates AND number_nights IS NOT NULL)",
            name="flexible_num_nights_required",
        ),
        CheckConstraint(
            "(NOT flexible_dates) OR (flexible_dates AND preferred_months IS NOT NULL)",
            name="flexible_months_required",
        ),
        CheckConstraint(
            "(NOT flexible_dates) OR (flexible_dates AND preferred_start_dow IS NOT NULL)",
            name="flexible_dow_required",
        ),
        CheckConstraint(
            "(flexible_dates) OR (NOT flexible_dates AND start_date IS NOT NULL)",
            name="exact_start_date_required",
        ),
        CheckConstraint(
            "(flexible_dates) OR (NOT flexible_dates AND end_date IS NOT NULL)",
            name="exact_end_date_required",
        ),
        CheckConstraint(
            "(number_attendees IS NOT NULL) OR ((number_attendees_range_lower IS NOT NULL) AND (number_attendees_range_upper IS NOT NULL))",
            name="number_attendees_info_required",
        ),
    )

    id = Column(Integer, primary_key=True)

    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc)
    )

    # Common data
    email = Column(String, nullable=False)
    company_name = Column(String)
    flexible_dates = Column(Boolean, nullable=False)
    occupancy_types = Column(JSONB)  # array of string values
    meeting_spaces = Column(JSONB)  # array of string values

    # backend now supports either number of attendees OR a lower-upper bound range
    number_attendees = Column(Integer)
    number_attendees_range_lower = Column(Integer)
    number_attendees_range_upper = Column(Integer)

    # Flexible dates data
    number_nights = Column(Integer)
    preferred_months = Column(JSONB)  # array of months (strings)
    preferred_start_dow = Column(JSONB)  # array of day's of week (strings)

    # Non-flexible dates data
    start_date = Column(Date)
    end_date = Column(Date)

    # Other data
    state = Column(String, default="intake")
    flok_owner = Column(String)
