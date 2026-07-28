from unittest.mock import Base

from sqlalchemy import Float, Integer
from sqlalchemy.orm import Mapped, mapped_column


class Soil(Base):
    __tablename__ = "soil"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    temperature: Mapped[float] = mapped_column(Float)
    moisture: Mapped[int] = mapped_column(Integer)

    # id = Column(Integer, primary_key=True)
    # outside_temperature = Column(Float, nullable=False)
    # inside_temperature = Column(Float, nullable=False)
    # moisture = Column(Integer, nullable=False)
    # timestamp= Column(DateTime, server_default=func.now())
