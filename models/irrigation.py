import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class SoilMeasurements(Base):
    __tablename__ = "soil_measurements"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    esp_id: Mapped[int] = mapped_column(ForeignKey("esp.id"))
    irrigation: Mapped[str] = mapped_column()
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    esp: Mapped["Esp"] = relationship()  # noqa: F821
