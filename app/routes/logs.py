from app.dependencies.auth import required_role
from fastapi import Depends, APIRouter, HTTPException, status, Query, Request
from app.services.logs import get_all_logs_from_mongo
from app.pagination import paginate

router = APIRouter()

@router.get("/get_logs/")
async def get_all_logs(request: Request,
                       pagination: bool = True,
                       user_data: dict = Depends(required_role(["super_admin"])),
                       page: int = Query(1, alias="page", ge=1),
                        page_size: int = Query(10, alias="page_size", ge=1, le=100)):
    try:
        logs = await get_all_logs_from_mongo()
        # Extract logs from the "counts" key
        if isinstance(logs, dict) and "counts" in logs:
            logs = logs["counts"]
        else:
            logs = []  # Fallback if "counts" key is missing
        paginated_logs = paginate(logs, page, page_size, request, pagination)
        return paginated_logs
        # return {"logs": logs}
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