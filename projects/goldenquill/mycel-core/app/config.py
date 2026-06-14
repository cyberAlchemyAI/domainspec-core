from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    port: int = 8000
    database_url: str = "sqlite:///mycel_audit.db"

    class Config:
        env_file = ".env"

settings = Settings()
