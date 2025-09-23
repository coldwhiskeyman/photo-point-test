from typing import Optional

from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from config import get_settings


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    telegram_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


settings = get_settings()
engine = create_engine(settings.get_database_url())
SessionLocal = sessionmaker(bind=engine)


def get_user(user_id: int) -> Optional[User]:
    with SessionLocal() as session:
        return session.get(User, user_id)



