from config import Config
from app import App
from routes.setup import setup_routes

def setup_app(config: Config) -> App:
    app = App(
        config = config.bot
    )

    setup_routes(app)

    return app

