from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, env_file=".env", env_file_encoding="utf-8")

    # APP CONFIG
    APP_VERSION: int = 1
    ENV: str = "development"
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    LOG_LEVEL: str = "info"
    FILES_PATH: str = "./temp"

    # DATABASE CONFIG
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "mindhub-dev"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DATABASE_NAME: str = "mindhub-dev"

    @property
    def DATABASE_URL(self) -> str:
        """Construct the PostgreSQL database URL for SQLAlchemy"""
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )

    # REDIS CONFIG
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # AWS S3 CONFIG
    AWS_ACCESS_KEY_ID: str = "test"
    AWS_SECRET_ACCESS_KEY: str = "test"
    AWS_REGION: str = "eu-west-1"
    AWS_BUCKET_NAME: str = "fazaconta"
    AWS_S3_URL: str = "http://localhost:4566"

    # JWT CONFIG
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_SECRET: str = "accesss_token_secret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours = 1440 minutes
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 86400
