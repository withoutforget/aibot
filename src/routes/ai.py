import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import Command

from src.routes.filter import RepliedToBotFilter

from chatgpt_md_converter import telegram_format
from dishka import FromDishka

from src.infra.user_resources.users import UserResoucres
from src.usecases.ai import ChatService

from enum import Enum


class TopicAction(Enum):
    TOPIC_START = 1
    TOPIC_CONTINUE = 2
    TOPIC_START_WITH_CONTEXT = 3


router = Router()


@router.message(Command(commands=["stats"]), RepliedToBotFilter())
async def get_topic_info(message: Message, chat_service: FromDishka[ChatService]):
    try:
        metadata = chat_service.get_metadata(message.reply_to_message.message_id)

        output = f"<a href='{metadata['topic_start']}'>Начало диалога</a>. Диалог был начат {metadata['topic_starter']}."

        await message.reply(text=output, parse_mode=ParseMode.HTML)
    except:
        await message.reply("К сожалению, информации о данном чате нет.")


async def manage_chat(
    message: Message,
    res: UserResoucres,
    chat_service: ChatService,
    action: ChatAction,
):
    text = message.text.lstrip("/ai")
    user = message.from_user

    if len(text) == 0:
        await message.reply("Вы ничего не написали.")
        return

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        message_thread_id=message.message_thread_id,
        action=ChatAction.TYPING,
    )

    match action:
        case TopicAction.TOPIC_START:
            result, uuid = chat_service.start_chat(msg=message)
        case TopicAction.TOPIC_CONTINUE:
            result, uuid = chat_service.continue_chat(message.reply_to_message, message)

    tokens_used = result.usage_metadata.total_token_count

    if not res.user_exist(user.id):
        res.add_user(user.id, user.username)

    res.increment_tokens(user.id, tokens_used)

    new_message = await message.reply(
        telegram_format(result.text), parse_mode=ParseMode.HTML
    )

    chat_service.include_messasge(uuid, new_message.message_id)

@router.message(Command(commands=["ai"]))
async def create_chat(
    message: Message,
    res: FromDishka[UserResoucres],
    chat_service: FromDishka[ChatService],
):
    await manage_chat(
        message=message,
        res=res,
        chat_service=chat_service,
        action=TopicAction.TOPIC_START,
    )


@router.message(RepliedToBotFilter())
async def continue_chat(
    message: Message,
    res: FromDishka[UserResoucres],
    chat_service: FromDishka[ChatService],
):
    try:
        await manage_chat(
            message=message,
            res=res,
            chat_service=chat_service,
            action=TopicAction.TOPIC_CONTINUE,
        )
    except Exception as e:
        logging.warning(f"Got exception: {e}")
        await message.reply(f"К сожалению данный чат истёк. Пожалуйста, начните новый.")


@router.message(Command(commands=["credits"]))
async def get_list_balance(message: Message, user_res: FromDishka[UserResoucres]):
    result = "Потрачено кредитов:"
    for user in sorted(
        user_res._data.values(), key=lambda u: u.tokens_used, reverse=True
    ):
        result += f"\nt.me/{user.username} - {user.tokens_used} ({user.promts_generated} messages);"
    await message.reply(result)
