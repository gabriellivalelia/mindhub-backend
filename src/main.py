# import uvicorn

# from infra.config.settings import Settings
# from infra.http.app import MindHubApp

# mind_hub_app = MindHubApp()
# app = mind_hub_app.app

# if __name__ == "__main__":
#     is_development = Settings().ENV == "development"

#     uvicorn.run(
#         "main:app",
#         host=Settings().HOST,
#         port=Settings().PORT,
#         reload=is_development,
#         log_level=Settings().LOG_LEVEL,
#     )
