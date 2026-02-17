import httpx
from fastapi import Depends, HTTPException, status, Request
from .auth import required_role
from app.utils import get_bearer_token, send_request, get_async_client

CURRENCY_CUNVERSION_URL = os.getenv("CURRENCY_CONVERSION_UPDATE_URL", "http://currency-conversion-service:8000/conversion-rates/")



async def get_all_currency_conversion_rates(request: Request, client: httpx.AsyncClient):
    """Retrieves all conversion rates from the currency conversion service."""
    token = get_bearer_token(request)
    return await send_request("GET", CURRENCY_CUNVERSION_URL, token, {}, client)