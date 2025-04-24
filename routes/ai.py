from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command
from infra.ai.ai import Chats, ChatObject
from routes.mid import ChatsMiddleware
from config import GeminiConfig, GeminiModelConfig

from chatgpt_md_converter import telegram_format
from time import time
import logging

router = Router()
router.message.middleware(ChatsMiddleware())


async def generate_ai_content(message: Message, chats: Chats, model: GeminiModelConfig) -> None:
    chats.expire_chats()
    try:
        text = message.text.lstrip('/ai ')
        if len(text) == 0:
            return 


        if message.reply_to_message is None or (
            message.reply_to_message is not None and message.reply_to_message.text is None
        ):
            co: ChatObject = chats.create_chat()
            #chats.update_chat(co.uuid)
        else:
            co = chats.find_chat(message.reply_to_message.message_id)
            if co is None:
                await message.reply('Время сеанса истекло. Пожалуйста, начните новый диалог.')
                return
        
        result_ai = co.chat.send_message(
            message=text,
            config = model.generate()
        ).text
        new_message = await message.reply( telegram_format(result_ai), parse_mode = ParseMode.HTML)
        co.messages.add(message.message_id)
        co.messages.add(new_message.message_id)
        co.last_time_used = time()
    except Exception as e:
        logging.info(f'Got exception ({e})')
        await message.reply(fr'Что-то пошло не так...\n({e})')
@router.message(Command(commands=['ai']))
async def gen_ai(message: Message, chats: Chats, gemini: GeminiConfig):
    await generate_ai_content(message, chats, gemini.basic)
    
@router.message(Command(commands=['fai']))
async def gen_ai(message: Message, chats: Chats, gemini: GeminiConfig):
    await generate_ai_content(message, chats, gemini.full) # not to use cause i don't wanna spend too much tokens
    