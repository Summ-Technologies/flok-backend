from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import Enum
from typing import List, Optional

from serde import deserialize, serialize
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import JSON

from . import base


class Retreat(base.Base):
    """Retreat table"""

    __tablename__ = "retreats"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False)

    selected_destinations = relationship(
        "SelectedDestination", order_by="SelectedDestination.created_at.desc()"
    )
    lodging_preferences = relationship(
        "LodgingPreference", order_by="LodgingPreference.created_at.desc()"
    )
    lodging_proposals = relationship("LodgingProposal")
    lodging_contracts = relationship("LodgingContract")
    employee_flights_trips = relationship("EmployeeFlightTrip")

    # Metadata
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc)
    )


class Destination(base.Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True)
    google_maps_id = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=False)


class LodgingPartner(base.Base):
    """LodgingPartner table (aka hotels)"""

    __tablename__ = "lodging_partners"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    image_url = Column(String)
    description = Column(String)
    contact = Column(String)


class SelectedDestination(base.Base):
    __tablename__ = "selected_destinations"
    id = Column(Integer, primary_key=True)
    retreat_id = Column(Integer, ForeignKey("retreats.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc)
    )


class LodgingPreference(base.Base):
    __tablename__ = "lodging_preferences"

    id = Column(Integer, primary_key=True)
    retreat_id = Column(Integer, ForeignKey("retreats.id"), nullable=False)
    num_employees = Column(Integer, nullable=False)
    dates = Column(JSON, nullable=False)  # either exact or im flexible
    meeting_space = Column(JSON, nullable=False)  # either exact or im flexible
    rooming_preferences = Column(JSON, nullable=False)  # either exact or im flexible
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc)
    )


@deserialize
@serialize
@dataclass
class Dates(object):
    class DateType(Enum):
        EXACT = "EXACT"
        FLEXIBLE = "FLEXIBLE"

    type: DateType
    exact_date_start: Optional[date]
    exact_date_end: Optional[date]
    flexible_nights: Optional[int]
    flexible_months: Optional[List[str]]
    flexible_start_day_preferences: Optional[List[str]]


@deserialize
@serialize
@dataclass
class MeetingSpace(object):
    class MeetingSpaceOption(Enum):
        FULLTEAM = "FULLTEAM"
        BREAKOUT = "BREAKOUT"

    selected: List[MeetingSpaceOption]


@deserialize
@serialize
@dataclass
class RoomingPreferences(object):
    class RoomingPreferencesOption(Enum):
        SINGLES = "SINGLES"
        DOUBLES = "DOUBLES"

    selected: RoomingPreferencesOption


class LodgingProposal(base.Base):
    __tablename__ = "lodging_proposals"

    id = Column(Integer, primary_key=True)
    retreat_id = Column(Integer, ForeignKey("retreats.id"))
    lodging_partner_id = Column(
        Integer, ForeignKey("lodging_partners.id"), nullable=False
    )
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    proposal_url = Column(String)

    lodging_parter = relationship("LodgingPartner")


class LodgingContract(base.Base):
    __tablename__ = "lodging_contracts"

    id = Column(Integer, primary_key=True)
    retreat_id = Column(Integer, ForeignKey("retreats.id"), nullable=False)
    lodging_partner_id = Column(
        Integer, ForeignKey("lodging_partners.id"), nullable=False
    )

    lodging_parter = relationship("LodgingPartner")
