from aiogram.filters.base import Filter
from aiogram.types import Message

class RepliedToBotFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.reply_to_message is not None and message.reply_to_message.from_user.id == message.bot.id