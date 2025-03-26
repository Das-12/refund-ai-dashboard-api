import httpx
from fastapi import Depends, HTTPException, status, Request
from .auth import required_role
from app.utils import get_bearer_token, send_request, get_async_client
from app.schemas.gst import GstCreate


GET_GST = "http://gst-service:8000/get/gst/"
GET_ALL_GST = "http://gst-service:8000/get_all_gst/"
CREATE_GST = "http://gst-service:8000/create_gst/"




async def get_gst_data(request: Request, client: httpx.AsyncClient, mac:str):
    """Retrieves conversion rate from the currency conversion service with mac id."""
    token = get_bearer_token(request)
    return await send_request("GET", GET_GST, token, {"mac": mac}, client)


async def get_all_gst_data(request: Request, client: httpx.AsyncClient):
    """list all conversion rates from the currency conversion service."""
    token = get_bearer_token(request)
    return await send_request("GET", GET_ALL_GST, token, {}, client)


async def create_gst(request: Request,gst_data:GstCreate, client: httpx.AsyncClient):
    """Retrieves all conversion rates from the currency conversion service."""
    token = get_bearer_token(request)
    return await send_request("POST", CREATE_GST, token, gst_data, client)
