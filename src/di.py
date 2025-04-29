from dishka import make_async_container, Provider, AsyncContainer, Scope, provide
from src.config import (
    Config,
    AIConfig,
    BotConfig,
    get_config,
    GeminiConfig,
    PostgresConfig,
)
from src.infra.ai.ai import Chats, ChatGenerator
from src.infra.user_resources.users import UserResoucres
from src.usecases.ai import ChatService
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.infra.sqlalchemy.models import Base
from typing import AsyncGenerator

class MyProvider(Provider):
    @provide
    async def _get_cfg(self) -> Config:
        return get_config()
    @provide(scope=Scope.APP)
    async def _get_chats_object(self, config: Config) -> Chats:
        return Chats(generator=ChatGenerator(config = config.ai.gemini), gemini=config.ai.gemini)

    @provide(scope=Scope.REQUEST)
    async def _get_user_res(
        self, session: AsyncSession
    ) -> UserResoucres:
        return UserResoucres(session=session)

    @provide(scope=Scope.APP)
    async def _get_chat_service(
        self, chats: Chats, config: Config
    ) -> ChatService:
        return ChatService(chats=chats, config=config.ai.gemini)

    @provide(scope=Scope.APP)
    async def _get_engine(self, config: Config) -> AsyncEngine:
        engine = AsyncEngine(
                sync_engine=create_engine(url=config.postgres.dsn())
            )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        return engine

    @provide(scope=Scope.APP)
    async def _get_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def _get_asyncsession(self, sm: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
        async with sm.begin() as session:
            yield session
    
        
        


def get_container() -> AsyncContainer:
    cont = make_async_container(MyProvider(scope=Scope.APP))
    return cont
