from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "MedRoute AI"
    APP_VERSION: str = "1.0.0"

    MODEL_PROVIDER: str = "colab"
    MODEL_ENDPOINT: str = ""
    MODEL_API_KEY: str = ""
    MODEL_TIMEOUT_SECONDS: float = 60.0
    MODEL_RETRY_ATTEMPTS: int = 3

    # MySQL is optional — database logging is not implemented yet
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DATABASE: str = "triage_db"

    class Config:
        env_file = ".env"


settings = Settings()
