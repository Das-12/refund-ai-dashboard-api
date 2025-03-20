from app.dependencies.subscriptions import (
    create_subscription, get_all_subscriptions, get_subscription_by_id, update_subscription, delete_subscription, get_async_client, required_role
)
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from app.pagination import paginate
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
    # print(f"sended to auth and this is type of start_date {type(subscription_data.start_date), subscription_data.start_date}")
    try:
        if auth_user.get("role") != "super_admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for your role")
        if subscription_data.start_date:
            subscription_data.start_date = subscription_data.start_date.isoformat()
        subscription_dict = subscription_data.model_dump()  

        subscription_out = await create_subscription(request, subscription_dict, client)
        return subscription_out
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/subscriptions", response_model = dict)
async def get_all_subscription(request: Request,
                                pagination: bool = True,
                                skip: int = Query(1, alias="skip", ge=1),
                                limit: int = Query(10, alias="limit", ge=1, le=100),
                                client: httpx.AsyncClient = Depends(get_async_client)):
    try:
        subscriptions_data = await get_all_subscriptions(request, client)
        pagination_data = paginate(subscriptions_data, skip, limit, request, pagination)
        return pagination_data
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