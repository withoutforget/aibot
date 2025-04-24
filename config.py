from dataclasses import dataclass
from dynaconf import Dynaconf
from adaptix import Retort

@dataclass(init=True)
class BotConfig:
    general_api_key: str
    debug_api_key: str 
    is_debug: bool

@dataclass(init=True)
class AIConfig:
    api_key: str
    model: str
    promt_file: str
    tokens: int
    temperature: float 

@dataclass(init=True)
class Config:
    bot: BotConfig
    ai: AIConfig

def get_config() -> Config:
    dyna = Dynaconf(
        settings_files = [ "./config/config.toml" ]
    )
    return dyna