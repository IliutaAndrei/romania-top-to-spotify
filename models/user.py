from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    spotify_id: Mapped[str] = mapped_column(unique=True)
    display_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    access_token: Mapped[str] = mapped_column()
    refresh_token: Mapped[str] = mapped_column()
    expires_at: Mapped[datetime] = mapped_column(DateTime)