import logging
import asyncio

from src.config import Config, get_config
from src.setup import setup_app, setup_logging
from src.di import get_container
from dishka.integrations.aiogram import setup_dishka


async def main() -> None:
    config: Config = get_config()
    app = setup_app(config)

    setup_dishka(container=get_container(), router=app.dp(), auto_inject=True)

    setup_logging()

    await app.dp().start_polling(app.bot())


if __name__ == "__main__":
    asyncio.run(main())
