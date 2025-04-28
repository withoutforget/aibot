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


class MyProvider(Provider):
    tmp = dict()

    @provide
    async def _get_cfg(self) -> Config:
        return get_config()

    @provide
    async def _get_ai_cfg(self, cfg: Config) -> AIConfig:
        return cfg.ai

    @provide
    async def _get_pg_cfg(self, cfg: Config) -> PostgresConfig:
        return cfg.postgres

    @provide
    async def _get_bot_cfg(self, cfg: Config) -> BotConfig:
        return cfg.bot

    @provide
    async def _get_gemini_cfg(self, cfg: Config) -> GeminiConfig:
        return cfg.ai.gemini

    @provide
    async def _get_chats_object(self, ai: AIConfig) -> Chats:
        if "chats" not in self.tmp.keys():
            self.tmp["chats"] = Chats(
                generator=ChatGenerator(config=ai.gemini), gemini=ai.gemini
            )
        return self.tmp["chats"]

    @provide
    async def _get_user_res(
        self, session: async_sessionmaker[AsyncSession]
    ) -> UserResoucres:
        if "user_res" not in self.tmp.keys():
            self.tmp["user_res"] = UserResoucres(session=session)
        return self.tmp["user_res"]

    @provide
    async def _get_chat_service(
        self, chats: Chats, config: GeminiConfig
    ) -> ChatService:
        if "chat_service" not in self.tmp.keys():
            self.tmp["chat_service"] = ChatService(chats=chats, config=config)
        return self.tmp["chat_service"]

    @provide
    async def _get_engine(self, postgres: PostgresConfig) -> AsyncEngine:
        if "async_engine" not in self.tmp.keys():
            self.tmp["async_engine"] = AsyncEngine(
                sync_engine=create_engine(url=postgres.dsn())
            )
            engine = self.tmp["async_engine"]

            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

        return self.tmp["async_engine"]

    @provide
    async def _get_connection(self, engine: AsyncEngine) -> AsyncConnection:
        if "async_conn" not in self.tmp.keys():
            self.tmp["async_conn"] = engine.connect()
        return self.tmp["async_conn"]

    @provide
    async def _get_session(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)


def get_container() -> AsyncContainer:
    cont = make_async_container(MyProvider(scope=Scope.APP))
    return cont
