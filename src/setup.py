from src.config import Config
from src.app import App
from src.routes.setup import setup_routes

def setup_app(config: Config) -> App:
    app = App(
        config = config.bot
    )

    setup_routes(app)

    return app

