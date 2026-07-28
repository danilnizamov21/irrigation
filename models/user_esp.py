from sqlalchemy import Column, ForeignKey, Integer, Table

from core.db import Base

user_esp_association = Table(
    "user_esp_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("esp_id", Integer, ForeignKey("esp.id"), primary_key=True),
)
