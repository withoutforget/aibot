from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command


router = Router()

@router.message(Command(commands=['ai_help']))
async def ai_help(message: Message):
    await message.reply("""Используйте /ai, чтобы сгенерировать ответ. Вы также можете продолжить переписку,
                        если ответите на одно из сообщений учавствующих в переписке (ваше или бота).""")