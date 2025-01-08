from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    debug: bool = False  

    MONGO_USERNAME: Optional[str] = None
    MONGO_PASSWORD: Optional[str] = None
    MONGO_HOST: str = "host.docker.internal"
    MONGO_PORT: int = 27017
    MONGO_AUTH_SOURCE: Optional[str] = None
    class Config:
        env_file = ".env"

settings = Settings()