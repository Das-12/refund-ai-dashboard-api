from app.dependencies.auth import required_role
from fastapi import Depends, APIRouter


router = APIRouter()


@router.get("/auth/")
async def admin_auth(user_data: dict = Depends(required_role(["admin"]))):
    return {"message": "you are admin", "user_data": user_data}