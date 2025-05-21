from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # DB SETTINGS
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str


    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # API URL
    API_URL: str

    WORKERS_AMOUNT: int
    DEBUG: bool

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
