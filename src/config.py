import os

from pydantic_settings import BaseSettings, SettingsConfigDict


DOTENV = os.path.join(os.path.dirname(__file__), '.env')


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    DB_HOST_TEST: str
    DB_PORT_TEST: int
    POSTGRES_USER_TEST: str
    POSTGRES_PASSWORD_TEST: str
    POSTGRES_DB_TEST: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}'

    @property
    def TEST_DATABASE_URL_asyncpg(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER_TEST}:{self.POSTGRES_PASSWORD_TEST}@{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.POSTGRES_DB_TEST}'

    model_config = SettingsConfigDict(env_file=DOTENV)


settings = Settings()
