from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.sqlalchemy.models import User
from sqlalchemy import select
import asyncio

TelegramID = int


@dataclass()
class UserData:
    username: str
    tokens_used: int = 0
    promts_generated: int = 0


class UserResoucres:
    _data: dict[TelegramID, UserData] = dict()
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def user_exist(self, id: TelegramID) -> bool:
        return id in self._data.keys()
    
    async def _user_exist(self, id: TelegramID) -> bool:
        stmt = select(User).where(User.telegram_id == id)
        return await self._session.scalar(stmt)

    async def add_user(self, id: TelegramID, username: str) -> bool:
        if not await self._user_exist(id):
            new_user = User(
                telegram_id = id,
                username = username,
                tokens_used = 0
            )

            self._session.add(new_user)

            await self._session.commit()
    
        if await self.user_exist(id):
            return False
        self._data[id] = UserData(username)
        return True

    async def increment_tokens(self, id: TelegramID, tokens: int) -> bool:
        if not await self.user_exist(id):
            return False
        self._data[id].tokens_used += tokens
        self._data[id].promts_generated += 1
        return True
    
    async def _get_all(self) -> list[str]:
        res = list()
        expr = select(User)
        for u in await self._session.scalars(expr):
            res.append(str(u))
        return res
