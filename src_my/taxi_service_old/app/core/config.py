from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # Grid
    GRID_N: int = 100
    GRID_M: int = 100
    T_CELL_SECONDS: int = 2

    # Timeouts
    ASSIGN_CONFIRM_TIMEOUT: int = 30

    # DB / Redis
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/taxi_db"
    REDIS_DSN: str = "redis://localhost:6379/0"

    # JWT
    JWT_SECRET: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24

    API_V1_PREFIX: str = "/api/v1"

    def access_token_expires(self):
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

settings = Settings()
