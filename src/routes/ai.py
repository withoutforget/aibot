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


@router.message(Command(commands=["del"]))
async def delete_dialog(message: Message, chat_service: FromDishka[ChatService]):
    try:

        count = message.text.removeprefix('/del ')
        if count.isdecimal():
            count = int(count)
        else:
            count = None

        message_ids = chat_service.get_history(message)
        if len(message_ids) == 0:
            await message.reply("Не могу удалить этот чат.")
            return
        if count is None:
            count = len(message_ids)
        message_ids = sorted(message_ids, reverse=True)[: count * 2]
        message_ids.append(message.message_id)
        await message.bot.delete_messages(chat_id=message.chat.id, message_ids=message_ids)
    
    except Exception as e:
        await message.reply(f'Что-то пошло не так: {e}')    


@router.message(Command(commands=["stats"]), RepliedToBotFilter())
async def get_topic_info(message: Message, chat_service: FromDishka[ChatService]):
    try:
        metadata = chat_service.get_metadata(message.reply_to_message.message_id)

        output = f"<a href='{metadata['topic_start']}'>Начало диалога</a>. Диалог был начат {metadata['topic_starter']}."

        await message.reply(text=output, parse_mode=ParseMode.HTML)
    except Exception as e:
        await message.reply(f"К сожалению, информации о данном чате нет. {e}")


async def manage_chat(
    message: Message,
    res: UserResoucres,
    chat_service: ChatService,
    action: ChatAction,
):
    text = message.text.removeprefix('/ai ')
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
        case TopicAction.TOPIC_START_WITH_CONTEXT:
            result, uuid = chat_service.start_chat(
                msg=message, context=message.reply_to_message.text
            )

    tokens_used = result.usage_metadata.total_token_count

    if not await res.user_exist(user.id):
        await res.add_user(user.id, user.username)

    await res.increment_tokens(user.id, tokens_used)

    new_message = await message.reply(
        telegram_format(result.text), parse_mode=ParseMode.HTML
    )

    chat_service.include_message(uuid, new_message.message_id)
    chat_service.include_message(uuid, message.message_id)


@router.message(Command(commands=["ai"]))
async def create_chat(
    message: Message,
    res: FromDishka[UserResoucres],
    chat_service: FromDishka[ChatService],
):
    action = TopicAction.TOPIC_START
    if message.reply_to_message is not None:
        if message.reply_to_message.text is not None:
            action = TopicAction.TOPIC_START_WITH_CONTEXT

    try:
        await manage_chat(
            message=message, res=res, chat_service=chat_service, action=action
        )
    except Exception as e:
        await message.reply(f"Что-то пошло не так... {e}")


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
        await message.reply(f"Что-то пошло не так. {e}")


@router.message(Command(commands=["credits"]))
async def get_list_balance(message: Message, user_res: FromDishka[UserResoucres]):
    try:
        result = "Потрачено кредитов:"

        users = await user_res.get_users()

        for user in sorted(users, key=lambda u: u.tokens_used, reverse=True):
            result += f"\nt.me/{user.username} - {user.tokens_used} ({user.message_count} messages);"
        await message.reply(result)
    except Exception as e:
        await message.reply(f'Что-то пошло не так: {e}')    

