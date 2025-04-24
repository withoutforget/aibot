from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message
from infra.ai.ai import Chats
from config import GeminiConfig

class ChatsMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        data['chats'] = await data['container'].get(Chats)
        data['gemini'] = await data['container'].get(GeminiConfig)
        return await handler(event, data)
