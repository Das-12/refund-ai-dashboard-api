from app.database import logs_collection
from fastapi import HTTPException, status
from app.models import MongoBaseModel

async def get_all_logs_from_mongo():
    try:
        logs = await logs_collection.find().to_list(length=None)
        
        print(f"Fetched logs from MongoDB: {logs}")
        
        return [MongoBaseModel.from_mongo(log) for log in logs]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching logs: {e}"
        )
