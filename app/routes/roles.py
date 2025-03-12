from app.dependencies.roles import (
    required_role, create_roles, assign_role, get_async_client, roles_from_token,
    roles_from_username, get_all_roles, update_role, delete_role
    )
from fastapi import Depends, APIRouter
from app.schemas.roles import RoleCreate, RoleOut, AssignRoleRequest, AssignRoleOut, MultiRoleOut
from fastapi import HTTPException, status, Request
import httpx
from typing import List
import logging

router = APIRouter()

@router.post("/create_role", response_model=RoleOut)
async def create_role(
    request: Request,
    role_data: RoleCreate,  # Pydantic model
    auth_user: dict = Depends(required_role(["super_admin"])),
    client: httpx.AsyncClient = Depends(get_async_client)
):
    if auth_user.get("role") != "super_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")
    try:
        role_dict = role_data.model_dump()  

        role_out = await create_roles(request, role_dict, client=client)
        return role_out
    except Exception as e:
        print(f"error is {str(e)}")
        raise HTTPException(status_code=404,detail=str(e))

@router.get("/roles", response_model = List[MultiRoleOut])
async def get_all_role(
    request: Request,
    client: httpx.AsyncClient = Depends(get_async_client)
):
    try:
        roles_data = await get_all_roles(request, client)
        return roles_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/assign_role", response_model=AssignRoleOut)
async def assign_roles(
    request: Request,
    role_data: AssignRoleRequest,  # Pydantic model
    auth_user: dict = Depends(required_role(["super_admin"])),
    client: httpx.AsyncClient = Depends(get_async_client)
):
    try:
        if auth_user.get("role") != "super_admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")

        role_dict = role_data.model_dump()  

        role_out = await assign_role(request, role_dict, client = client)
        return role_out
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/get_user_role_token", response_model=AssignRoleOut)
async def get_user_role_token(
    request: Request,
    client: httpx.AsyncClient = Depends(get_async_client)
):
    try:
        role_out = await roles_from_token(request, client = client)
        
        return role_out
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/roles/{username}", response_model=AssignRoleOut)
async def dashboard_get_user_roles(
    username: str,
    request: Request,
    client: httpx.AsyncClient = Depends(get_async_client)
):
    """
    Dashboard endpoint that returns the roles for a given username.
    """
    try:
        roles_data = await roles_from_username(request, username, client)
        return roles_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.put("/update_role/{role_id}", response_model=dict)
async def dashboard_update_role(role_id: int,
                                request: Request,
                                role_data: RoleCreate,
                                auth_user: dict = Depends(required_role(["super_admin"])),
                                client: httpx.AsyncClient = Depends(get_async_client)):
    print("dashboard update role started")
    """
    Dashboard endpoint that updates a role.
    """
    try:
        if auth_user.get("role") != "super_admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")
        role_dict = role_data.model_dump() 
        updated_role = await update_role(request, role_id, role_dict, client)
        # print(f"this is updated role in dashboard {updated_role}")
        return updated_role
    except Exception as e:
        # Log the actual error and return an internal server error response
        logging.error(f"Unexpected error getting user roles: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail={str(e)}  # Return the actual error message
        )


@router.delete("/delete_role/{role_id}", response_model=dict)
async def dashboard_delete_role(role_id: int,
                                request: Request,
                                auth_user: dict = Depends(required_role(["super_admin"])),
                                client: httpx.AsyncClient = Depends(get_async_client)):
    """
    Dashboard endpoint that deletes a role.
    """
    try:
        if auth_user.get("role") != "super_admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")
        
        delete = await delete_role(request, role_id, client)
        return delete
    
    except Exception as e:
        # Log the actual error and return an internal server error response
        logging.error(f"Unexpected error getting user roles: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail={str(e)}  # Return the actual error message
        )
    
    
    
