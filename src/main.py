import uvicorn

from infra.config.settings import Settings
from infra.http.app import MindHubApp

mind_hub_app = MindHubApp()
app = mind_hub_app.app

if __name__ == "__main__":
    settings = Settings()
    is_development = settings.ENV == "development"

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload_dirs=["src"] if is_development else None,
        reload=is_development,
        log_level=settings.LOG_LEVEL,
    )
