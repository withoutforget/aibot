from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.sqlalchemy.models import User
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import async_sessionmaker
import asyncio

TelegramID = int

class UserResoucres:
    _session: async_sessionmaker[AsyncSession]

    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self._session = session

    async def _get_user(self, id : TelegramID) -> User | None:
        async with self._session.begin() as session:
            stmt = select(User).where(User.telegram_id == id)
            res = await session.execute(stmt)
            await session.flush()
            return res.scalar()

    async def user_exist(self, id: TelegramID) -> bool:
        return await self._get_user(id) is not None

    async def add_user(self, id: TelegramID, username: str) -> bool:
        if await self.user_exist(id):
            return False
        async with self._session.begin() as session:
            session.add(
                User(
                    telegram_id = id,
                    username = username,
                    tokens_used = 0,
                    message_count = 0,
                )
            )
            await session.flush()
            return True
        

    async def increment_tokens(self, id: TelegramID, tokens: int) -> bool:
        u = await self._get_user(id)
        if u is None:
            return False
        async with self._session.begin() as session:
            stmt = (
                update(User)
                .where(User.telegram_id == id)
                .values(tokens_used=User.tokens_used + tokens)
                .values(message_count=User.message_count + 1)
            )
            await session.execute(stmt)
            await session.flush()
        return True
    
    async def get_users(self) -> list[User]:
        stmt = select(User)
        async with self._session.begin() as session:
            res = await session.execute(stmt)
            ret = []
            for i in res.scalars():
                ret.append(i)
            await session.flush()
            return ret
        