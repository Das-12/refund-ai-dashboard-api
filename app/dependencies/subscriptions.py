import httpx
from fastapi import Depends, HTTPException, status, Request
from .auth import required_role
from app.utils import get_bearer_token, send_request, get_async_client
import json

CREATE_SUBSCRIPTIONS = "http://authentication-service:8000/subscriptions/subscriptions"

async def create_subscription(
    request: Request,
    subscription_data: dict,
    client: httpx.AsyncClient
):
    """Creates subscriptions by forwarding the request to the authentication service."""
    token = get_bearer_token(request)
    return await send_request("POST", CREATE_SUBSCRIPTIONS, token, subscription_data, client)

async def get_all_subscriptions(
    request: Request,
    client: httpx.AsyncClient
):
    """Retrieves all subscriptions from the authentication service."""
    token = get_bearer_token(request)
    return await send_request("GET", CREATE_SUBSCRIPTIONS, token, {}, client)

async def get_subscription_by_id(
    request: Request,
    subscription_id: int,
    client: httpx.AsyncClient
):
    """Retrieves a subscription by id from the authentication service."""
    token = get_bearer_token(request)
    url = f"http://authentication-service:8000/subscriptions/subscriptions/{subscription_id}"
    return await send_request("GET", url, token, {}, client)

async def update_subscription(
    request: Request,
    subscription_id: int,
    subscription_data: dict,
    client: httpx.AsyncClient
):
    """Updates a subscription by id from the authentication service."""
    token = get_bearer_token(request)
    url = f"http://authentication-service:8000/subscriptions/subscriptions/{subscription_id}"
    return await send_request("PUT", url, token, subscription_data, client)

async def delete_subscription(
    request: Request,
    subscription_id: int,
    client: httpx.AsyncClient
):
    """Deletes a subscription by id from the authentication service."""
    token = get_bearer_token(request)
    url = f"http://authentication-service:8000/subscriptions/subscriptions/{subscription_id}"
    return await send_request("DELETE", url, token, {}, client)