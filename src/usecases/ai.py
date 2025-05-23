from src.infra.ai.ai import Chats, Chat, ChatObject
from aiogram.types import Message
from google.genai.types import GenerateContentResponse
from src.config import GeminiConfig
from uuid import UUID


class ChatService:
    _chats: Chats
    _gemini: GeminiConfig

    def __init__(self, chats: Chats, config: GeminiConfig):
        self._chats = chats
        self._gemini = config

    def _format_request(self, msg: Message, context: str = "") -> str:
        return self._gemini.format_string.format(
            username=msg.from_user.username,
            text=msg.text,
            context=context,
        )

    def _send_to_chat_with(self, msg: Message, chat: Chat, context: str = ""):
        request = self._format_request(msg, context)

        config = self._gemini.basic.generate()

        result = chat.send_message(message=request, config=config)

        return result

    def start_chat(
        self, msg: Message, context: str = ""
    ) -> tuple[GenerateContentResponse, UUID]:
        new_chat = self._chats.create_chat()
        new_chat.topic_starter_username = f"@{msg.from_user.username}"

        msg_link = f"{str(msg.chat.id).removeprefix('-100')}/"
        if msg.message_thread_id is not None:
            msg_link += f"{msg.message_thread_id}/"
        msg_link += f"{msg.message_id}"

        new_chat.link_to_topic_start = f"t.me/c/{msg_link}"

        result = self._send_to_chat_with(msg, new_chat.chat, context)

        return result, new_chat.uuid

    def include_message(self, uuid: UUID, message_id: int):
        self._chats.get_chat(uuid).messages.add(message_id)

    def continue_chat(
        self, old_msg: Message, new_message: Message
    ) -> tuple[GenerateContentResponse, UUID]:
        self._chats.expire_chats()
        chat: ChatObject = self._chats.find_chat(old_msg.message_id)
        result = self._send_to_chat_with(new_message, chat.chat)
        self._chats.update_chat(chat.uuid)
        return result, chat.uuid

    def get_metadata(self, message_id: int) -> dict:
        chat = self._chats.find_chat(message_id)
        if chat is not None:
            return {
                "topic_start": chat.link_to_topic_start,
                "topic_starter": chat.topic_starter_username,
            }
        return {}

    def get_history(self, message: Message) -> list[int]:
        msg = None
        if message.reply_to_message is not None:
            if message.reply_to_message.from_user.id == message.bot.id:
                msg = message.reply_to_message
        if msg is None:
            return []
        msg: Message = msg
        co = self._chats.find_chat(msg.message_id)
        if co is None:
            return []
        return list(co.messages)
