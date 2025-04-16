from pydantic_settings import BaseSettings


class Config(BaseSettings):
    BOT_TOKEN: str
    POSTGRES_PORT: int = 5432
    POSTGRES_URL: str = "localhost"
    POSTGRES_USER: str = "myuser"
    POSTGRES_PASSWORD: str  = "mypassword"
    POSTGRES_DB: str  = "mydatabase"
    REDIS_URL: str | None
    REDIS_ENABLED: bool = False

    class Config:
        env_file = '.env'


# Читаем конфигурацию
config = Config()
