from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

# MONGO_DETAILS = f"mongodb://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}:{settings.MONGO_PORT}/admin?authSource={settings.MONGO_AUTH_SOURCE}"
MONGO_DETAILS = f"mongodb://{settings.MONGO_HOST}:{settings.MONGO_PORT}/"
if settings.MONGO_USERNAME and settings.MONGO_PASSWORD:
    MONGO_DETAILS = (
        f"mongodb://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@"
        f"{settings.MONGO_HOST}:{settings.MONGO_PORT}/admin?authSource={settings.MONGO_AUTH_SOURCE}"
    )
    
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.cache_log
logs_collection = database.get_collection("logs")
counts_collection = database.get_collection("counts")
auth_collection = database.get_collection("auth_logs")
api_collection = database.get_collection("api_logs")
gst_collection = database.get_collection("gst_logs")
app_error_collection = database.get_collection("app_errors")