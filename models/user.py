from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from models.user_esp import user_esp_association


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, nullable=False)
    hash_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(
        String, default="user"
    )  # user, admin, super-admin
    esps: Mapped[list["Esp"]] = relationship(  # noqa: F821
        secondary=user_esp_association, back_populates="users"
    )
