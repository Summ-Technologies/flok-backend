from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey

from . import base


class Employee(base.Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String)
    location = Column(String)
    preferred_airport = Column(String)
