import httpx
from fastapi import Depends, HTTPException, status, Request
from .auth import required_role
from app.utils import get_bearer_token, send_request, get_async_client

CREATE_PLAN = "http://authentication-service:8000/subscriptions/plans"


async def create_plan(
    request: Request,
    plan_data: dict,
    client: httpx.AsyncClient
):
    """Creates plans by forwarding the request to the authentication service."""
    token = get_bearer_token(request)
    return await send_request("POST", CREATE_PLAN, token, plan_data, client)

async def get_all_plans(
    request: Request,
    client: httpx.AsyncClient
):
    """Retrieves all plans from the authentication service."""
    token = get_bearer_token(request)
    return await send_request("GET", CREATE_PLAN, token, {}, client)

async def get_plan_by_id(
    request: Request,
    plan_id: int,
    client: httpx.AsyncClient
):
    """Retrieves a plan by id from the authentication service."""
    token = get_bearer_token(request)
    url = f"http://authentication-service:8000/subscriptions/plans/{plan_id}"
    return await send_request("GET", url, token, {}, client)

async def update_plan(
    request: Request,
    plan_id: int,
    plan_data: dict,
    client: httpx.AsyncClient
):
    """Updates a plan by id from the authentication service."""
    token = get_bearer_token(request)
    url = f"http://authentication-service:8000/subscriptions/plans/{plan_id}"
    return await send_request("PUT", url, token, plan_data, client)

async def delete_plan(
    request: Request,
    plan_id: int,
    client: httpx.AsyncClient
):
    """Deletes a plan by id from the authentication service."""
    token = get_bearer_token(request)
    url = f"http://authentication-service:8000/subscriptions/plans/{plan_id}"
    return await send_request("DELETE", url, token, {}, client)