from dataclasses import dataclass
from dynaconf import Dynaconf
from adaptix import Retort

from google.genai.types import GenerateContentConfig


@dataclass(init=True)
class BotConfig:
    general_api_key: str
    debug_api_key: str
    is_debug: bool


@dataclass(init=True)
class GeminiModelConfig:
    promt_file: str
    tokens: int
    temperature: float

    def generate(self):
        return GenerateContentConfig(
            system_instruction=open(self.promt_file).read(),
            max_output_tokens=self.tokens,
            temperature=self.temperature,
        )


@dataclass(init=True)
class GeminiConfig:
    api_key: str
    model: str
    format_string: str

    basic: GeminiModelConfig
    full: GeminiModelConfig


@dataclass(init=True)
class AIConfig:
    gemini: GeminiConfig


@dataclass(init=True)
class Config:
    bot: BotConfig
    ai: AIConfig


def get_config() -> Config:
    dyna = Dynaconf(settings_files=["./config/config.toml", "./config/.secrets.toml"])
    cfg = Retort().load(dyna, Config)
    return cfg
