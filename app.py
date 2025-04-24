from aiogram import Bot, Dispatcher
from config import BotConfig, Config

class App:
    config: BotConfig
    def __init__(self, config: BotConfig):
        self.config = config    
        self._bot = Bot(
            token = self.config.debug_api_key
        )
        self._dp = Dispatcher(

        )

    def bot(self) -> Bot:
        return self._bot
    
    def dp(self) -> Dispatcher:
        return self._dp 
    