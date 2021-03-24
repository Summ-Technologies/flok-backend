from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import JSON, Boolean

from . import base


class UserLoginProvider(base.Base):
    """UserLoginProvider"""

    __tablename__ = "users_login_providers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    provider = Column(
        String, nullable=False
    )  # one of hawk_models.auth.UserLoginProviderType
    unique_id = Column(String, nullable=False)  # typically email (based on provider)
    data = Column(
        JSON, nullable=True
    )  # have a feeling only will be needed for custom login (holding password hash)

    def __repr__(self):
        return f"UserLoginProvider(id={self.id},user_id={self.user_id},provider={self.provider},unique_id={self.unique_id})"


class UserLoginId(base.Base):
    __tablename__ = "users_login_ids"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # core data
    login_id = Column(String, unique=True, default=lambda: str(uuid4()))
    is_active = Column(Boolean, nullable=False, default=True)

    # relationship
    user = relationship("User")

    # metadata
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc)
    )


class UserLoginToken(base.Base):
    __tablename__ = "users_login_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # core data
    login_token = Column(String, unique=True, default=lambda: str(hash(uuid4())))
    is_active = Column(Boolean, nullable=False, default=True)

    # relationship

    # metadata
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc)
    )
