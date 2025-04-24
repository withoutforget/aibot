from app import App

from routes.ai import router as ai_router

def setup_routes(app: App) -> None:
    app.dp().include_routers(
        ai_router
    )