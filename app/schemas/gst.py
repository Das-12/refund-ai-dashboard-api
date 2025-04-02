from pydantic import BaseModel
from typing import Optional
from datetime import datetime




class GstCreate(BaseModel):
    mac: str
    raf: float
    gst_economy: float
    gst_premium_economy: float
    gst_business: float
    gst_first: float
    reissue_tax_code: str
    refund_tax_code: str
    non_refundable_taxes: str
    market: str
    class Config:
        from_attributes = True