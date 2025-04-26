from dishka import make_async_container, Provider, AsyncContainer, Scope, provide
from src.config import Config, AIConfig, BotConfig, get_config, GeminiConfig
from src.infra.ai.ai import Chats, ChatGenerator
from src.infra.user_resources.users import UserResoucres
from src.usecases.ai import ChatService


class MyProvider(Provider):
    tmp = dict()

    @provide
    async def _get_cfg(self) -> Config:
        return get_config()

    @provide
    async def _get_ai_cfg(self, cfg: Config) -> AIConfig:
        return cfg.ai

    @provide
    async def _get_bot_cfg(self, cfg: Config) -> BotConfig:
        return cfg.bot

    @provide
    async def _get_gemini_cfg(self, cfg: Config) -> GeminiConfig:
        return cfg.ai.gemini

    @provide
    async def _get_chats_object(self, ai: AIConfig) -> Chats:
        if "chats" not in self.tmp.keys():
            self.tmp["chats"] = Chats(generator=ChatGenerator(config=ai.gemini))
        return self.tmp["chats"]

    @provide
    async def _get_user_res(self) -> UserResoucres:
        if "user_res" not in self.tmp.keys():
            self.tmp["user_res"] = UserResoucres()
        return self.tmp["user_res"]

    @provide
    async def _get_chat_service(
        self, chats: Chats, config: GeminiConfig
    ) -> ChatService:
        if "chat_service" not in self.tmp.keys():
            self.tmp["chat_service"] = ChatService(chats=chats, config=config)
        return self.tmp["chat_service"]


def get_container() -> AsyncContainer:
    cont = make_async_container(MyProvider(scope=Scope.APP))
    return cont
