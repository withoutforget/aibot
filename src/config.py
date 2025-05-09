from dataclasses import dataclass
from dynaconf import Dynaconf
from adaptix import Retort, name_mapping

from google.genai.types import GenerateContentConfig

from sqlalchemy import URL

import logging

@dataclass(slots=True)
class BotConfig:
    general_api_key: str
    debug_api_key: str
    is_debug: bool


@dataclass(slots=True)
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


@dataclass(slots=True)
class GeminiConfig:
    api_key: str
    model: str
    format_string: str
    chat_timeout: int

    basic: GeminiModelConfig
    full: GeminiModelConfig


@dataclass(slots=True)
class AIConfig:
    gemini: GeminiConfig


@dataclass(slots=True)
class PostgresConfig:
    dbname: str
    username: str
    password: str

    def dsn(self) -> str:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.username,
            password=self.password,
            database=self.dbname,
            host="postgres",
            port=5432,
        ).render_as_string(False)

    @property
    def pdsn(self) -> str:
        return self.dsn()


@dataclass(slots=True)
class Config:
    bot: BotConfig
    ai: AIConfig
    postgres: PostgresConfig


def get_config() -> Config:
    dyna = Dynaconf(
        settings_files=["./config/config.toml", '.env'],
           load_dotenv=True,
            environments=True,
            default_env="default",
            merge_enabled=True,
            env_switcher="AIBOT_ENV"
        )
    
    retort = Retort(
        
    )


    cfg = retort.load(dyna, Config)

    return cfg
