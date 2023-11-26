from apps.base.database import Base
from sqlalchemy import Column, Integer, DateTime, func


class FastModel(Base):
    """Base model with predefined fields."""

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(
        DateTime,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
