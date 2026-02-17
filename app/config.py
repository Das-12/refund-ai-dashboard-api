from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    debug: bool = False  

    # MONGO_USERNAME: Optional[str] = None
    # MONGO_PASSWORD: Optional[str] = None
    # MONGO_HOST: str = "host.docker.internal"
    # MONGO_PORT: int = 27017
    # MONGO_AUTH_SOURCE: Optional[str] = None
    
    MONGO_USERNAME:str = os.getenv("MONGO_USERNAME", 'admin')
    MONGO_PASSWORD:str = os.getenv("MONGO_PASSWORD",'KldkhhmS%23392')
    MONGO_HOST:str = os.getenv("MONGO_HOST",'206.189.91.84')
    MONGO_PORT:int = os.getenv("MONGO_PORT",'27017')
    MONGO_AUTH_SOURCE:str = os.getenv("MONGO_AUTH_SOURCE",'admin')
    
    KAFKA_BROKER_URL: str = os.getenv("KAFKA_BROKER_URL",'159.89.199.213:9092')
    KAFKA_USERNAME: str = os.getenv("KAFKA_USERNAME",'arshad')
    KAFKA_PASSWORD: str = os.getenv("KAFKA_PASSWORD",'KldkhhmS392')
    KAFKA_TOPIC:str = os.getenv("KAFAKA_TOPIC",'auth_logging')
    KAFKA_APP_ERROR_TOPIC:str = os.getenv("KAFKA_APP_ERROR_TOPIC",'app_error')
        
    class Config:
        env_file = ".env"

settings = Settings()