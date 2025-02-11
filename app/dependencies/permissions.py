import httpx
from fastapi import Depends, HTTPException, status, Request
import logging
from .auth import required_role
from app.utils import get_bearer_token, send_request, get_async_client

CREATE_PERMISSION = "http://authentication-service:8000/permissions/permissions"
PERMISSIONS_FROM_TOKEN = "http://authentication-service:8000/permissions/get-user-permission-token"
ASSIGN_PERMISSION = "http://authentication-service:8000/permissions/assign-permission"
GET_PERMISSIONS = "http://authentication-service:8000/permissions/permissions"

async def create_permissions(
    request: Request,
    permission_data: dict,
    client: httpx.AsyncClient
):
    """Creates permissions by forwarding the request to the authentication service."""
    token = get_bearer_token(request)
    return await send_request("POST", CREATE_PERMISSION, token, permission_data, client)

async def assign_permission(
    request: Request,
    permission_data: dict,
    client: httpx.AsyncClient
):
    """Assigns permissions by forwarding the request to the authentication service."""
    token = get_bearer_token(request)
    return await send_request("POST", ASSIGN_PERMISSION, token, permission_data, client)

async def permissions_from_token(
    request: Request,
    client: httpx.AsyncClient
):
    """Retrieves permissions for the user from the token."""
    token = get_bearer_token(request)
    return await send_request("GET", PERMISSIONS_FROM_TOKEN, token, {}, client)

async def permissions_from_username(
    request: Request,
    username: str,
    client: httpx.AsyncClient
) -> dict:
    """
    Retrieves permissions for the given username from the authentication service.
    """
    token = get_bearer_token(request)
    url = f"http://authentication-service:8000/permissions/permissions/{username}"
    return await send_request("GET", url, token, {}, client)

async def get_permissions(
    request: Request,
    client: httpx.AsyncClient
):
    """Retrieves all permissions from the authentication service."""
    token = get_bearer_token(request)
    return await send_request("GET", GET_PERMISSIONS, token, {}, client)