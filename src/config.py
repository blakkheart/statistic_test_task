import os

from pydantic_settings import BaseSettings, SettingsConfigDict


DOTENV = os.path.join(os.path.dirname(__file__), '.env')


class Settings(BaseSettings):
	DB_HOST: str
	DB_PORT: int
	POSTGRES_USER: str
	POSTGRES_PASSWORD: str
	POSTGRES_DB: str

	@property
	def DATABASE_URL_asyncpg(self):
		return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}'

	model_config = SettingsConfigDict(env_file=DOTENV)


settings = Settings()
