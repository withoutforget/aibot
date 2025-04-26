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

    def _send_to_chat(self, msg: Message, chat: Chat):
        request = self._gemini.format_string.format(
            username=msg.from_user.username, text=msg.text
        )

        config = self._gemini.basic.generate()

        result = chat.send_message(message=request, config=config)

        return result

    def start_chat(self, msg: Message) -> tuple[GenerateContentResponse, UUID]:
        new_chat = self._chats.create_chat()
        result = self._send_to_chat(msg, new_chat.chat)
        return result, new_chat.uuid

    def include_messasge(self, uuid: UUID, message_id: int):
        self._chats.get_chat(uuid).messages.add(message_id)

    def continue_chat(
        self, old_msg: Message, new_message: Message
    ) -> tuple[GenerateContentResponse, UUID]:
        chat: ChatObject = self._chats.find_chat(old_msg.message_id)
        result = self._send_to_chat(new_message, chat.chat)
        return result, chat.uuid
