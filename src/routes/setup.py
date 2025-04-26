from src.app import App

from src.routes.ai import router as ai_router
from src.routes.help import router as help_router


def setup_routes(app: App) -> None:
    app.dp().include_routers(ai_router, help_router)
