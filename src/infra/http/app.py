from fastapi import FastAPI


class MindHubApp:
    __app: FastAPI

    def __init__(self):
        self.__app = FastAPI(
            title="MindHub",
            version="1.0.0",
            docs_url="/docs",
            summary="API do MindHub",
        )

    @property
    def app(self) -> FastAPI:
        return self.__app
