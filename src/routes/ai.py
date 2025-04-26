from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import Command

from src.routes.filter import RepliedToBotFilter

from chatgpt_md_converter import telegram_format
from dishka import FromDishka

from src.infra.user_resources.users import UserResoucres
from src.usecases.ai import ChatService

router = Router()


@router.message(Command(commands=["ai"]))
async def create_chat(
    message: Message,
    res: FromDishka[UserResoucres],
    chat_service: FromDishka[ChatService],
):
    text = message.text.lstrip("/ai")
    user = message.from_user

    if len(text) == 0:
        await message.reply("Вы ничего не написали.")
        return

    try:
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            message_thread_id=message.message_thread_id,
            action=ChatAction.TYPING,
        )

        result, uuid = chat_service.start_chat(msg=message)

        tokens_used = result.usage_metadata.total_token_count

        if not res.user_exist(user.id):
            res.add_user(user.id, user.username)

        res.increment_tokens(user.id, tokens_used)

        new_message = await message.reply(
            telegram_format(result.text), parse_mode=ParseMode.HTML
        )

        chat_service.include_messasge(uuid, new_message.message_id)

    except Exception as e:
        await message.reply(f"Что-то пошло не так... ({e})")


@router.message(RepliedToBotFilter())
async def continue_chat(
    message: Message,
    res: FromDishka[UserResoucres],
    chat_service: FromDishka[ChatService],
):
    user = message.from_user
    try:
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            message_thread_id=message.message_thread_id,
            action=ChatAction.TYPING,
        )

        result, uuid = chat_service.continue_chat(message.reply_to_message, message)

        tokens_used = result.usage_metadata.total_token_count

        if not res.user_exist(user.id):
            res.add_user(user.id, user.username)

        res.increment_tokens(user.id, tokens_used)

        new_message = await message.reply(
            telegram_format(result.text), parse_mode=ParseMode.HTML
        )

        chat_service.include_messasge(uuid, new_message.message_id)
    except Exception as e:
        await message.reply(f"Что-то пошло не так... ({e})")


@router.message(Command(commands=["ai_list"]))
async def get_list_balance(message: Message, user_res: FromDishka[UserResoucres]):
    result = "Потрачено кредитов:"
    for user in sorted(
        user_res._data.values(), key=lambda u: u.tokens_used, reverse=True
    ):
        result += f"\nt.me/{user.username} - {user.tokens_used} ({user.promts_generated} messages);"
    await message.reply(result)
