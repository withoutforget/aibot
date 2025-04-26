from src.config import Config
from src.app import App
from src.routes.setup import setup_routes
from time import time

import logging


def setup_logging(show_all_loggers=False, disable_all_except_aiogram=True):
    log_file_path = f"./logs/{int(time())}.log"

    open(log_file_path, "x").close()

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] - %(message)s",
        datefmt="%d/%b/%Y %H:%M:%S",
        handlers=[
            logging.FileHandler(filename=log_file_path),
            logging.StreamHandler(),
        ],
    )

    if show_all_loggers:
        loggers = [name for name in logging.root.manager.loggerDict.keys()]

        logging.info(f"Current loggers: {loggers!r}")

    if disable_all_except_aiogram:
        for kName in logging.root.manager.loggerDict:
            if kName.startswith("aiogram"):
                continue
            logging.getLogger(kName).disabled = True


def setup_app(config: Config) -> App:
    app = App(config=config.bot)

    setup_routes(app)

    return app
