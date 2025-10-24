from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from .constants import DEFAULT_STAGE
from .database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True, unique=True)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    stage = Column(String, nullable=False, default=DEFAULT_STAGE)
    source = Column(String, nullable=False, default="manual")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
