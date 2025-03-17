from app.dependencies.subscriptions import (
    create_subscription, get_all_subscriptions, get_subscription_by_id, update_subscription, delete_subscription, get_async_client, required_role
)
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.schemas.subscriptions import SubscriptionCreate, SubscriptionResponse, SubscriptionUpdate
import httpx
from typing import List

router = APIRouter()

@router.post("/create_subscription", response_model=SubscriptionResponse)
async def create_subscriptions(
    request: Request,
    subscription_data: SubscriptionCreate,
    auth_user: dict = Depends(required_role(["super_admin"])),
    client: httpx.AsyncClient = Depends(get_async_client)   
):
    try:
        if auth_user.get("role") != "super_admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")
        
        subscription_dict = subscription_data.model_dump()  

        subscription_out = await create_subscription(request, subscription_dict, client)
        return subscription_out
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/subscriptions", response_model = List[SubscriptionResponse])
async def get_all_subscription(
    request: Request,
    client: httpx.AsyncClient = Depends(get_async_client)
):
    try:
        subscriptions_data = await get_all_subscriptions(request, client)
        return subscriptions_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/subscriptions/{subscription_id}", response_model = SubscriptionResponse)
async def get_subscription_by_ids(
    request: Request,
    subscription_id: int,
    auth_user: dict = Depends(required_role(["super_admin"])),
    client: httpx.AsyncClient = Depends(get_async_client)
):
    try:
        if auth_user.get("role") != "super_admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")
        
        subscription_data = await get_subscription_by_id(request, subscription_id, client)
        return subscription_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.put("/subscriptions/{subscription_id}", response_model = SubscriptionResponse)
async def update_subscriptions(
    request: Request,
    subscription_id: int,
    subscription_data: SubscriptionUpdate,
    auth_user: dict = Depends(required_role(["super_admin"])),
    client: httpx.AsyncClient = Depends(get_async_client)
):
    try:
        if auth_user.get("role") != "super_admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")
        
        subscription_dict = subscription_data.model_dump()  

        subscription_out = await update_subscription(request, subscription_id, subscription_dict, client)
        return subscription_out
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/subscriptions/{subscription_id}", response_model = SubscriptionResponse)
async def delete_subscriptions(
    request: Request,
    subscription_id: int,
    auth_user: dict = Depends(required_role(["super_admin"])),
    client: httpx.AsyncClient = Depends(get_async_client)
):
    try:
        if auth_user.get("role") != "super_admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")
        
        subscription_data = await delete_subscription(request, subscription_id, client)
        return subscription_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")