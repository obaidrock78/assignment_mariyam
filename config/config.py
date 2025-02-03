from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "sqlite:///database.db"

    class Config:
        extra = "allow"


settings = Settings()
