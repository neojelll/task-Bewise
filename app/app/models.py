from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Application(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
