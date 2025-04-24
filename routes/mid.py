from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message
from infra.ai.ai import Chats


class ChatsMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        data['chats'] = await data['container'].get(Chats)
        return await handler(event, data)
