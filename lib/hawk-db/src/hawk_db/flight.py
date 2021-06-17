from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DECIMAL

from . import base


class FlightTrip(base.Base):
    __tablename__ = "flight_trips"
    id = Column(Integer, primary_key=True)
    travel_time = Column(Integer, nullable=False)  # in minutes

    flight_legs = relationship("FlightLeg")


class FlightLeg(base.Base):
    __tablename__ = "flight_legs"

    id = Column(Integer, primary_key=True)

    flight_trip_id = Column(Integer, ForeignKey("flight_trips.id"), nullable=False)
    leg_order = Column(Integer, nullable=False)  # keeps order for legs in a flight trip

    flight_number = Column(String, nullable=False)
    from_airport = Column(String, nullable=False)
    to_airport = Column(String, nullable=False)
    departure_at = Column(DateTime(timezone=True), nullable=False)
    arrival_at = Column(DateTime(timezone=True), nullable=False)
    flight_time = Column(Integer)  # in minutes


class EmployeeFlightTrip(base.Base):
    __tablename__ = "employees_to_flight_trips"

    arrival_flight_trip_id = Column(
        Integer, ForeignKey("flight_trips.id"), nullable=False
    )
    departure_flight_trip_id = Column(
        Integer, ForeignKey("flight_trips.id"), nullable=False
    )
    employee_id = Column(Integer, ForeignKey("employees.id"), primary_key=True)
    retreat_id = Column(Integer, ForeignKey("retreats.id"), primary_key=True)
    est_cost = Column(Integer, nullable=False)  # in cents
    final_cost = Column(Integer, nullable=False)  # in cents
    status = Column(String, nullable=False)  # pending approval, pending booking, booked
    url = Column(String)

    arrival_flight_trip = relationship(
        "FlightTrip", foreign_keys=[arrival_flight_trip_id]
    )
    departure_flight_trip = relationship(
        "FlightTrip", foreign_keys=[departure_flight_trip_id]
    )
