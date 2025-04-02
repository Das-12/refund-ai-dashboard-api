from app.dependencies.auth import required_role
from fastapi import Depends, APIRouter, HTTPException, status, Query, Request
from app.services.logs import get_all_logs_from_mongo
from app.pagination import paginate

router = APIRouter()

# @router.get("/get_logs/")
# async def get_all_logs(request: Request,
#                        log_key: str = None,
#                        pagination: bool = True,
#                        user_data: dict = Depends(required_role(["super_admin"])),
#                        skip: int = Query(1, alias="skip", ge=1),
#                        limit: int = Query(10, alias="limit", ge=1, le=100)):
#     try:
#         print(f"this is log_key in route: {log_key}")
#         logs = await get_all_logs_from_mongo(log_key=log_key)
#         print(f"this is the type of logs: {type(logs)}")
#         # Extract logs from the "counts" key
#         if logs is not None:
#             paginated_logs = paginate(logs, skip, limit, request, pagination)
#             return paginated_logs
#         else:
#             logs = []
#  # Fallback if "counts" key is missing

#         # return {"logs": logs}
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    
@router.get("/get_logs/")
async def get_all_logs(
    request: Request,
    log_key: str = None,
    user_data: dict = Depends(required_role(["super_admin"])),
    skip: int = Query(0, alias="skip", ge=0),  # Start from 0
    limit: int = Query(10, alias="limit", ge=1, le=100)
):
    try:
        print(f"Fetching logs for: {log_key}, skip: {skip}, limit: {limit}")
        logs = await get_all_logs_from_mongo(request=request, log_key=log_key, skip=skip, limit=limit)  # Fetch only paginated data
        return logs if logs else {"logs": []}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    
    
# @router.get("/get_logs/")
# async def get_all_logs(user_data: dict = Depends(required_role(["super_admin"]))):
#     print("get logs started")
#     try:
#         logs = await get_all_logs_from_mongo()
#         return {"logs": logs}
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")