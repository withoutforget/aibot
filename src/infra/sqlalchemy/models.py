from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, BigInteger
from src.infra.sqlalchemy.basemodel import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "foo"}

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger(), unique=True)
    username: Mapped[str] = mapped_column(String(128))
    tokens_used: Mapped[int] = mapped_column(BigInteger())
    message_count: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"User({self.id=!r},{self.telegram_id=!r},{self.tokens_used!r})"
