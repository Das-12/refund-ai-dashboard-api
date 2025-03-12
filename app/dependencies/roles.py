import httpx
from fastapi import Depends, HTTPException, status, Request
import logging
from .auth import required_role
from app.utils import get_bearer_token, send_request, get_async_client
import json

CREATE_ROLE = "http://authentication-service:8000/permissions/roles"
ASSIGN_ROLE = "http://authentication-service:8000/permissions/assign-role"
ROLES_FROM_TOKEN = "http://authentication-service:8000/permissions/get-user-role-token"
GET_ALL_ROLES = "http://authentication-service:8000/permissions/roles"


async def create_roles(
    request: Request,
    role_data: dict,
    client: httpx.AsyncClient
):
    """Creates roles by forwarding the request to the authentication service."""
    token = get_bearer_token(request)
    return await send_request("POST", CREATE_ROLE, token, role_data, client)

async def get_all_roles(
    request: Request,
    client: httpx.AsyncClient
):
    """Retrieves all roles from the authentication service."""
    token = get_bearer_token(request)
    return await send_request("GET", GET_ALL_ROLES, token, {}, client)

async def assign_role(
    request: Request,
    role_data: dict,
    client: httpx.AsyncClient
):
    """Assigns roles by forwarding the request to the authentication service."""
    token = get_bearer_token(request)
    return await send_request("POST", ASSIGN_ROLE, token, role_data, client)

async def roles_from_token(
    request: Request,
    client: httpx.AsyncClient
):
    """Retrieves roles for the user from the token."""
    token = get_bearer_token(request)
    return await send_request("GET", ROLES_FROM_TOKEN, token, {}, client)

async def roles_from_username(
    request: Request,
    username: str,
    client: httpx.AsyncClient
) -> dict:
    """
    Retrieves roles for the given username from the authentication service.
    """
    token = get_bearer_token(request)
    url = f"http://authentication-service:8000/permissions/roles/{username}"
    return await send_request("GET", url, token, {}, client)

async def update_role(request: Request, role_id: int, role_data: dict, client: httpx.AsyncClient):
    """
    Updates role from the authentication service.
    """
    token = get_bearer_token(request)
    url = f"http://authentication-service:8000/permissions/update_role/{role_id}"
    return await send_request("PUT", url, token, role_data, client)


async def delete_role(request: Request, role_id: int, client: httpx.AsyncClient):
    """
    Updates role from the authentication service.
    """
    token = get_bearer_token(request)
    url = f"http://authentication-service:8000/permissions/delete_role/{role_id}"
    return await send_request("DELETE", url, token, {}, client) 