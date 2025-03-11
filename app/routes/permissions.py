from app.dependencies.permissions import (
    required_role, create_permissions, permissions_from_token, get_async_client, permissions_from_username,
    assign_permission, get_permissions
    )

from fastapi import Depends, APIRouter
from app.schemas.permission import permissionCreate, permissionOut, AssignPermissionsOut, AssignPermissionRequest, AssignPermissionResponse
from fastapi import HTTPException, status, Request
import httpx
from typing import List

router = APIRouter()

@router.post("/create_permission", response_model=permissionOut)
async def create_permission(
    request: Request,
    permission_data: permissionCreate,
    auth_user: dict = Depends(required_role(["super_admin"])),
    client: httpx.AsyncClient = Depends(get_async_client)
):
    try:
        if auth_user.get("role") != "super_admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")
        
        permission_dict = permission_data.model_dump()
        
        permission_out = await create_permissions(request, permission_dict, client = client)
        return permission_out
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/get_permissions", response_model = List[permissionOut])
async def get_permission(
    request: Request,
    client: httpx.AsyncClient = Depends(get_async_client)
):
    try:
        permission_out = await get_permissions(request, client = client)
        
        return permission_out
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/assign_permission", response_model=AssignPermissionResponse)
async def assign_permissions(
    request: Request,
    permission_data: AssignPermissionRequest,
    auth_user: dict = Depends(required_role(["super_admin"])),
    client: httpx.AsyncClient = Depends(get_async_client)
):
    try:
        if auth_user.get("role") != "super_admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")
        
        permission_dict = permission_data.model_dump()
        
        permission_out = await assign_permission(request, permission_dict, client = client)
        return permission_out
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/get_user_permission_token", response_model=AssignPermissionsOut)
async def get_user_permission_token(
    request: Request,
    client: httpx.AsyncClient = Depends(get_async_client)
):
    try:
        permission_out = await permissions_from_token(request, client = client)
        
        return permission_out
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/permissions/{username}", response_model=AssignPermissionsOut)
async def dashboard_get_user_permissions(
    username: str,
    request: Request,
    client: httpx.AsyncClient = Depends(get_async_client)
):
    try:
        permission_out = await permissions_from_username(request, username, client = client)
        
        return permission_out
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")