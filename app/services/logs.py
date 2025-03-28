from app.database import logs_collection, counts_collection, auth_collection, api_collection, gst_collection, app_error_collection
from fastapi import HTTPException, status

async def get_all_logs_from_mongo(log_key: str):
    print(f"this is log_key: {log_key}")
    try:
        print(f"this is log_key: {log_key}")
        if log_key == "logs":
            logs = await logs_collection.find().to_list(length=None)
            cleaned_logs = [{key: value for key, value in item.items() if key != '_id'} for item in logs]
            return cleaned_logs
        elif log_key == "counts":
            counts = await counts_collection.find().to_list(length=None)
            cleaned_counts = [{key: value for key, value in item.items() if key != '_id'} for item in counts]
            return cleaned_counts
        elif log_key == "auth_logs":
            auth_logs = await auth_collection.find().to_list(length=None)
            cleaned_auth_logs = [{key: value for key, value in item.items() if key != '_id'} for item in auth_logs]
            return cleaned_auth_logs
        elif log_key == "api_logs":
            api_logs = await api_collection.find().to_list(length=None)
            cleaned_api_logs = [{key: value for key, value in item.items() if key != '_id'} for item in api_logs]
            return cleaned_api_logs
        elif log_key == "gst_logs":
            gst_logs = await gst_collection.find().to_list(length=None)
            cleaned_gst_logs = [{key: value for key, value in item.items() if key != '_id'} for item in gst_logs]
            return cleaned_gst_logs
        elif log_key == "error_logs":
            error_logs = await app_error_collection.find().to_list(length=None)
            cleaned_error_logs = [{key: value for key, value in item.items() if key != '_id'} for item in error_logs]
            return cleaned_error_logs
        elif log_key is None:   
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