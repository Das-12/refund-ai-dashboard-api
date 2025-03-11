from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.schemas.currency_conversion import CurrencyConversionRate
import httpx
from typing import List, Optional
from datetime import datetime
from app.dependencies.plans import get_async_client
from app.dependencies.currency_conversion import get_all_currency_conversion_rates

router = APIRouter()



@router.get("/conversion_rates")
async def get_all_conversion_rates(
    request: Request,
    client: httpx.AsyncClient = Depends(get_async_client),
):
    rates_data = await get_all_currency_conversion_rates(request, client)

    return rates_data
 