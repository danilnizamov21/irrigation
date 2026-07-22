from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


class Esp(Base):
    __tablename__ = "esp"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
