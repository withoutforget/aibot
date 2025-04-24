from dishka import make_async_container, Provider, AsyncContainer, Scope, provide
from app import App
from config import Config, AIConfig, BotConfig, get_config, GeminiConfig
from dataclasses import dataclass
from infra.ai.ai import Chats, ChatGenerator

class MyProvider(Provider):    
    tmp = dict()

    @provide
    async def _get_cfg(self) -> Config:
        return get_config()
    
    @provide
    async def _get_ai_cfg(self, cfg: Config) -> AIConfig:
        return cfg.ai
    
    @provide 
    async def _get_bot_cfg(self, cfg : Config) -> BotConfig:
        return cfg.bot 
    
    @provide
    async def _get_gemini_cfg(self, cfg: Config) -> GeminiConfig:
        return cfg.ai.gemini
    
    @provide
    async def _get_chats_object(self, ai: AIConfig) -> Chats:
        if 'chats' in self.tmp.keys():
            return self.tmp['chats']

        obj =  Chats(
            generator = ChatGenerator(
                config = ai.gemini
            )
        )

        self.tmp['chats'] = obj 

        return obj
    
from aiogram.dispatcher.middlewares.base import BaseMiddleware

class DishkaMiddleware(BaseMiddleware):
    def __init__(self, container: AsyncContainer):
        self.container = container
    
    async def __call__(self, handler, event, data):
        data['container'] = self.container
        return await handler(event, data)

def setup_dishka(app: App):
    cont = make_async_container(
        MyProvider(scope = Scope.APP)
    )
    app.dp().message.middleware(DishkaMiddleware(container = cont))
