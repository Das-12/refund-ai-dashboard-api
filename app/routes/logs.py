from app.dependencies.auth import required_role
from fastapi import Depends, APIRouter
from app.services.logs import get_all_logs_from_mongo

router = APIRouter()

@router.get("/get_logs/")
async def get_all_logs(user_data: dict = Depends(required_role(["super_admin"]))):
    logs = await get_all_logs_from_mongo()
    return {"logs": logs}