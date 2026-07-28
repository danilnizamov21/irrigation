from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from models.user_esp import user_esp_association


class Esp(Base):
    __tablename__ = "esp"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    hashed_api_key: Mapped[str] = mapped_column(unique=True, index=True)
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    users: Mapped[list["User"]] = relationship(  # noqa: F821
        secondary=user_esp_association, back_populates="esps"
    )
