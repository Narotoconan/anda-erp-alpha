from sqlalchemy import Column, DateTime
from sqlalchemy import func
from app.core.database import Base


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment="更新时间")
j