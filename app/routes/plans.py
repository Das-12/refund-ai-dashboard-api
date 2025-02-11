from app.dependencies.plans import (
    create_plan, get_all_plans, get_plan_by_id, update_plan, delete_plan, get_async_client, required_role
)
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.schemas.plans import PlanCreate, Plan, PlanUpdate
import httpx
from typing import List

router = APIRouter()

@router.post("/create_plan", response_model=Plan)
async def create_plan(
    request: Request,
    plan_data: PlanCreate,
    auth_user: dict = Depends(required_role(["super_admin"])),
    client: httpx.AsyncClient = Depends(get_async_client)
):
    if auth_user.get("role") != "super_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")
    
    plan_dict = plan_data.model_dump()  

    plan_out = await create_plan(request, plan_dict, client)
    return plan_out

@router.get("/plans", response_model = List[Plan])
async def get_all_plans(
    request: Request,
    client: httpx.AsyncClient = Depends(get_async_client)
):
    plans_data = await get_all_plans(request, client)
    return plans_data

@router.get("/plans/{plan_id}", response_model = Plan)
async def get_plan_by_id(
    request: Request,
    plan_id: int,
    auth_user: dict = Depends(required_role(["super_admin"])),
    client: httpx.AsyncClient = Depends(get_async_client)
):
    if auth_user.get("role") != "super_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")
    
    plan_data = await get_plan_by_id(request, plan_id, client)
    return plan_data

@router.put("/plans/{plan_id}", response_model = Plan)
async def update_plan(
    request: Request,
    plan_id: int,
    plan_data: PlanUpdate,
    auth_user: dict = Depends(required_role(["super_admin"])),
    client: httpx.AsyncClient = Depends(get_async_client)
):
    if auth_user.get("role") != "super_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")
    
    plan_dict = plan_data.model_dump()  

    plan_out = await update_plan(request, plan_id, plan_dict, client)
    return plan_out

@router.delete("/plans/{plan_id}", response_model = Plan)
async def delete_plan(
    request: Request,
    plan_id: int,
    auth_user: dict = Depends(required_role(["super_admin"])),
    client: httpx.AsyncClient = Depends(get_async_client)
):
    if auth_user.get("role") != "super_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")
    
    plan_data = await delete_plan(request, plan_id, client)
    return plan_data