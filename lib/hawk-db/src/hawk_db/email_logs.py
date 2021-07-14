from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey

from . import base

class EmailLogs(base.Base):
    __tablename__ = "email_logs"
    id = Column(Integer, primary_key=True)
    date_added = Column(String)
    email_id = Column(String)
