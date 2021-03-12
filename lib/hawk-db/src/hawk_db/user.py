from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from . import base


class User(base.Base):
    """User table"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(String, nullable=False, unique=True)
    first_name = Column(String)
    last_name = Column(String)

    # Metadata
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc)
    )

    # Relationships
    login_provider = relationship("UserLoginProvider")

    def __repr__(self):
        return f"User(id={self.id},email={self.email},first_name={self.first_name},last_name={self.last_name})"
