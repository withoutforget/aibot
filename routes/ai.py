from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command
from infra.ai.ai import Chats, ChatObject
from routes.mid import ChatsMiddleware

from chatgpt_md_converter import telegram_format

import logging

router = Router()
router.message.middleware(ChatsMiddleware())

@router.message(Command(commands=["ai"]))
async def generate_ai_content(message: Message, chats: Chats) -> None:
    chats.expire_chats()
    try:
        text = message.text.lstrip('/ai ')
        if len(text) == 0:
            return 


        if message.reply_to_message is None or (
            message.reply_to_message is not None and message.reply_to_message.text is None
        ):
            co: ChatObject = chats.create_chat()
            chats.update_chat(co.uuid)
        else:
            print(message.reply_to_message)
            co = chats.find_chat(message.reply_to_message.message_id)
            if co is None:
                await message.reply('Диалог истёк. Начните заново')
                return
        
        result_ai = co.chat.send_message(text).text
        new_message = await message.reply( telegram_format(result_ai), parse_mode = ParseMode.HTML)
        co.messages.add(message.message_id)
        co.messages.add(new_message.message_id)
    except Exception as e:
        logging.info(f'Got exception ({e})')
        await message.reply(fr'Что-то пошло не так...\n({e})')