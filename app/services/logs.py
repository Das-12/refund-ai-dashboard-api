from app.database import logs_collection, counts_collection, auth_collection, api_collection, gst_collection
from fastapi import HTTPException, status

async def get_all_logs_from_mongo():
    try:
        logs = await logs_collection.find().to_list(length=None)
        counts = await counts_collection.find().to_list(length=None)
        auth_logs = await auth_collection.find().to_list(length=None)
        api_logs = await api_collection.find().to_list(length=None)
        gst_logs = await gst_collection.find().to_list(length=None)

        cleaned_logs = [{key: value for key, value in item.items() if key != '_id'} for item in logs]
        cleaned_counts = [{key: value for key, value in item.items() if key != '_id'} for item in counts]
        cleaned_auth_logs = [{key: value for key, value in item.items() if key != '_id'} for item in auth_logs]
        cleaned_api_logs = [{key: value for key, value in item.items() if key != '_id'} for item in api_logs]
        cleaned_gst_logs = [{key: value for key, value in item.items() if key != '_id'} for item in gst_logs]

        combined_logs = {
            "logs": cleaned_logs,
            "counts": cleaned_counts,
            "auth_logs": cleaned_auth_logs,
            "api_logs": cleaned_api_logs,
            "gst_logs": cleaned_gst_logs,
        }

        return combined_logs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching logs: {e}"
        )