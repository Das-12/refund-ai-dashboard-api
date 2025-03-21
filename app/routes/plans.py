from app.dependencies.plans import (
    create_plan, get_all_plans, get_plan_by_id, update_plan, delete_plan, get_async_client, required_role
)
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from app.schemas.plans import PlanCreate, Plan, PlanUpdate
import httpx
from typing import List
from app.pagination import paginate

router = APIRouter()

@router.post("/create_plan", response_model=Plan)
async def create_plans(
    request: Request,
    plan_data: PlanCreate,
    auth_user: dict = Depends(required_role(["super_admin"])),
    client: httpx.AsyncClient = Depends(get_async_client)
):
    # print("plan create dashboard started")
    try:
        if auth_user.get("role") != "super_admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")
        
        plan_dict = plan_data.model_dump()  

        plan_out = await create_plan(request, plan_dict, client)
        return plan_out
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/plans", response_model = dict)
async def get_all_plan(request: Request,
                        pagination: bool = True,
                        skip: int = Query(1, alias="skip", ge=1),
                        limit: int = Query(10, alias="limit", ge=1, le=100),
                        client: httpx.AsyncClient = Depends(get_async_client)):
    try:
        plans_data = await get_all_plans(request, client)
        pagination_data = paginate(plans_data, skip, limit, request, pagination)
        return pagination_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/plans/{plan_id}", response_model = Plan)
async def get_plan_by_ids(
    request: Request,
    plan_id: int,
    auth_user: dict = Depends(required_role(["super_admin"])),
    client: httpx.AsyncClient = Depends(get_async_client)
):
    try:
        if auth_user.get("role") != "super_admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")
        
        plan_data = await get_plan_by_id(request, plan_id, client)
        return plan_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.put("/plans/{plan_id}", response_model = Plan)
async def update_plans(
    request: Request,
    plan_id: int,
    plan_data: PlanUpdate,
    auth_user: dict = Depends(required_role(["super_admin"])),
    client: httpx.AsyncClient = Depends(get_async_client)
):
    try:
        if auth_user.get("role") != "super_admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")
        
        plan_dict = plan_data.model_dump()  

        plan_out = await update_plan(request, plan_id, plan_dict, client)
        return plan_out
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/plans/{plan_id}", response_model = dict)
async def delete_plans(
    request: Request,
    plan_id: int,
    auth_user: dict = Depends(required_role(["super_admin"])),
    client: httpx.AsyncClient = Depends(get_async_client)
):
    try:
        if auth_user.get("role") != "super_admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")
        
        plan_data = await delete_plan(request, plan_id, client)
        return plan_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")