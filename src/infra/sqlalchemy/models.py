from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer(), unique=True)
    username: Mapped[str] = mapped_column(String(128))
    tokens_used: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"User({self.id=!r},{self.telegram_id=!r},{self.tokens_used!r})"
