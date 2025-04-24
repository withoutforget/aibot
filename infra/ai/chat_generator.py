from google.genai import Client
from google.genai.chats import Chat
from google.genai.types import GenerateContentConfig
from config import AIConfig

class ChatGenerator:
    config: AIConfig
    client: Client 
    def __init__(self, config: AIConfig):
        self.config = config 
        self.client = Client(
            api_key = self.config.api_key
        )

    def create_chat(self) -> Chat:
        return self.client.chats.create(
            model = self.config.model,
            config = GenerateContentConfig(
                system_instruction = open(self.config.promt_file).read(),
                max_output_tokens=self.config.tokens,
                temperature=self.config.temperature
            )
        )
    

