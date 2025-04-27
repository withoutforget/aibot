from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command


router = Router()


@router.message(Command(commands=["help"]))
async def ai_help(message: Message):
    commands = {
        "/ai": "Позволяет начать новый диалог с ИИ. Если ответить сообщение, которое было в диалоге, то он продолжиться.",
        "/credits": "Показывает количество потраченных токенов всеми участниками бота.",
        "/stats": "Показывает статистику диалога, если указать команду в ответе на сообщение бота.",
        "/help": "Показывает man.",
    }

    await message.reply("Используйте /ai, чтобы начать диалог.")
