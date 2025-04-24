from google.genai import Client
from google.genai.chats import Chat
from config import GeminiConfig

class ChatGenerator:
    config: GeminiConfig
    client: Client 
    def __init__(self, config: GeminiConfig):
        self.config = config 
        self.client = Client(
            api_key = self.config.api_key
        )

    def create_chat(self) -> Chat:
        return self.client.chats.create(
            model = self.config.model,
            config = self.config.basic.generate()
        )
    

