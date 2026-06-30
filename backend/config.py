from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    MODEL_PROVIDER: str
    MODEL_ENDPOINT: str = ""
    MODEL_API_KEY: str = ""
    MODEL_TIMEOUT_SECONDS: float = 60.0
    MODEL_RETRY_ATTEMPTS: int = 3

    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str

    class Config:
        env_file = ".env"


settings = Settings()


