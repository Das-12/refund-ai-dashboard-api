from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    debug: bool = False  

    # MONGO_USERNAME: Optional[str] = None
    # MONGO_PASSWORD: Optional[str] = None
    # MONGO_HOST: str = "host.docker.internal"
    # MONGO_PORT: int = 27017
    # MONGO_AUTH_SOURCE: Optional[str] = None
    
    MONGO_USERNAME:str = 'admin'
    MONGO_PASSWORD:str = 'KldkhhmS%23392'
    MONGO_HOST:str = '206.189.91.84'
    MONGO_PORT:int = 27017
    MONGO_AUTH_SOURCE:str = 'admin'
    
    KAFKA_TOPIC = 'auth_logging'
    KAFKA_APP_ERROR_TOPIC = 'app_error'
        
    class Config:
        env_file = ".env"

settings = Settings()