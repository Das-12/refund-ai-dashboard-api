from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from app.schemas.currency_conversion import CurrencyConversionRate
import httpx
from typing import List, Optional
from datetime import datetime
from app.dependencies.plans import get_async_client
from app.dependencies.currency_conversion import get_all_currency_conversion_rates
from app.pagination import paginate

router = APIRouter()



@router.get("/conversion_rates")
async def get_all_conversion_rates(
    request: Request,
    pagination: bool = True,
    skip: int = Query(1, alias="skip", ge=1),
    limit: int = Query(10, alias="limit", ge=1, le=100),
    client: httpx.AsyncClient = Depends(get_async_client),
):
    rates_data = await get_all_currency_conversion_rates(request, client)
    paginated_logs = paginate(rates_data, skip, limit, request, pagination)
    return paginated_logs