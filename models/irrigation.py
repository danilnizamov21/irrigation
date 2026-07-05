
from sqlalchemy import Column, DateTime, Float, Integer, String, func
from core.db import Base


class Soil(Base):
    __tablename__ = "soil"
    id = Column(Integer, primary_key=True)
    outside_temperature = Column(Float, nullable=False)
    inside_temperature = Column(Float, nullable=False)
    moisture = Column(Integer, nullable=False)
    timestamp= Column(DateTime, server_default=func.now())