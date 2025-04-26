import logging 
import asyncio

from src.config import Config, get_config
from src.setup import setup_app
from src.di import get_container
from dishka.integrations import aiogram as di_aio

async def main() -> None:
    config: Config = get_config()
    app = setup_app(config)
    di_aio.setup_dishka(
        container= get_container(),
         router = app.dp(),
         auto_inject=True
           )
    

    await app.dp().start_polling(app.bot())

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    asyncio.run(main())