from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql.expression import true

from . import base


class EmailLog(base.Base):
    __tablename__ = "email_logs"
    id = Column(Integer, primary_key=True)
    email_id = Column(String, nullable=False)
    date_added = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(tz=timezone.utc),
    )
