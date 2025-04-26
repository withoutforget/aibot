from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command


router = Router()


@router.message(Command(commands=["ai_help"]))
async def ai_help(message: Message):
    await message.reply("Используйте /ai, чтобы начать диалог.")
