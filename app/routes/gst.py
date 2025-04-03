from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
import httpx
from typing import List, Optional
from datetime import datetime
from app.dependencies.plans import get_async_client
from app.pagination import paginate
from app.dependencies.gst import get_gst_data, get_all_gst_data, create_gst, update_gst
from app.schemas.gst import GstCreate, GstUpdate



router = APIRouter()


@router.get("/get_gst")
async def get_gst_endpoint(request: Request, mac: str, client: httpx.AsyncClient = Depends(get_async_client)):
    """
    Get GST data for a given MAC address.
    """
    try:
        gst_data = await get_gst_data(request, client, mac)
        return gst_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
        

@router.get("/get_all_gst")
async def get_all_gst_endpoint(request: Request,
                               pagination: bool = True,
                                skip: int = Query(1, alias="skip", ge=1),
                                limit: int = Query(10, alias="limit", ge=1, le=100),
                               client: httpx.AsyncClient = Depends(get_async_client)):
    """
    Get all GST data.
    """
    try:
        gst_data = await get_all_gst_data(request, client)
        pagination_data = paginate(gst_data, skip, limit, request, pagination)
        return pagination_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
        

@router.post("/create_gst")
async def create_gst_endpoint(request: Request,gst_data: GstCreate, client: httpx.AsyncClient = Depends(get_async_client)):
    """
    Create a new GST data entry.
    """
    try:
        gst_dict = gst_data.dict()
        gst_out = await create_gst(request, gst_dict, client)
        return gst_out
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/update_gst")
async def update_gst_endpoint(request: Request, mac: str, gst_data: GstUpdate, client: httpx.AsyncClient = Depends(get_async_client)):
    """
    Update GST data for a given MAC address.
    """
    try:
        gst_dict = gst_data.dict()
        gst_out = await update_gst(request, mac, gst_dict, client)
        return gst_out
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )