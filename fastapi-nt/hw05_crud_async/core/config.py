from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:7799@localhost:5432/shop_db"

    class Config: 
        env_file = ".env"


settings = Settings()