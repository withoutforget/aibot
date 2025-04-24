import logging 
import asyncio

from config import Config, get_config
from setup import setup_app
from di import setup_dishka

async def main() -> None:
    config: Config = get_config()
    app = setup_app(config)
    setup_dishka(app)

    await app.dp().start_polling(app.bot())

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    asyncio.run(main())