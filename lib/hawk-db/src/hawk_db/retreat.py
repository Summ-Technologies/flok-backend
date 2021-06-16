from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import JSON
from typing_extensions import Required, get_origin

from . import base


class Retreat(base.Base):
    """Retreat table"""

    __tablename__ = "retreats"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False)

    # destination selection
    # lodging preferences
    # lodging proposals
    # lodging contracts
    # employee_flights_trips

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


class LodgingProposal(base.Base):
    __tablename__ = "lodging_proposals"

    id = Column(Integer, primary_key=True)
    lodging_partner = Column(Integer, ForeignKey("lodging_partners.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    proposal_url = Column(String)


class LodgingContracts(base.Base):
    __tablename__ = "lodging_contracts"

    id = Column(Integer, primary_key=True)
    retreat_id = Column(Integer, ForeignKey("retreats.id"), nullable=False)
    lodging_partner = Column(Integer, ForeignKey("lodging_partners.id"), nullable=False)
