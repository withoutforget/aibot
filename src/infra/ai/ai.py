from dataclasses import dataclass
from src.config import GeminiConfig
from google.genai.chats import Chat
from src.infra.ai.chat_generator import ChatGenerator
from uuid import uuid4, UUID
from time import time


@dataclass(init=True)
class ChatObject:
    uuid: UUID
    chat: Chat
    last_time_used: int
    messages: set[int]
    link_to_topic_start: str
    topic_starter_username: str


class Chats:
    generator: ChatGenerator
    gemini: GeminiConfig
    _chats: list[ChatObject] = []

    def __init__(self, generator: ChatGenerator, gemini: GeminiConfig):
        self.generator = generator
        self.gemini = gemini

    def find_chat(self, message_id: int) -> ChatObject | None:
        for co in self._chats:
            if message_id in co.messages:
                return co

    def get_chat(self, uuid: UUID) -> ChatObject | None:
        for co in self._chats:
            if co.uuid == uuid:
                return co

    def create_chat(self) -> ChatObject:
        co = ChatObject(
            uuid=uuid4(),
            chat=self.generator.create_chat(),
            last_time_used=time(),
            messages=set(),
            link_to_topic_start="",
            topic_starter_username="",
        )
        self._chats.append(co)
        return self._chats[-1]

    def update_chat(self, uuid: UUID):
        co = self.get_chat(uuid)
        co.last_time_used = time()

    def expire_chats(self):
        for co in self._chats:
            if co.last_time_used + self.gemini.chat_timeout < time():
                self._chats.remove(co)
