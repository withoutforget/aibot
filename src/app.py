from aiogram import Bot, Dispatcher
from src.config import BotConfig


class App:
    config: BotConfig

    def __init__(self, config: BotConfig):
        self.config = config
        if self.config.is_debug:
            api_key = self.config.debug_api_key
        else:
            api_key = self.config.general_api_key
        self._bot = Bot(token=api_key)
        self._dp = Dispatcher()

    def bot(self) -> Bot:
        return self._bot

    def dp(self) -> Dispatcher:
        return self._dp
