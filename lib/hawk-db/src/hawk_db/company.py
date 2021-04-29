from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from . import base


class Company(base.Base):
    """Company table"""

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=True)

    # Metadata
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc)
    )

    admins = relationship(
        "User",
        secondary="companies_admins",
        primaryjoin="User.id==CompanyAdmin.admin_id",
        secondaryjoin="Company.id==CompanyAdmin.company_id",
    )


class CompanyAdmin(base.Base):
    """Company to company admin table"""

    __tablename__ = "companies_admins"

    # Relationships
    admin_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), primary_key=True)
    admin = relationship("User")
    company = relationship("Company")
