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
        
class GstUpdate(BaseModel):
    mac: Optional[str] = None
    raf: Optional[float] = None
    gst_economy: Optional[float] = None
    gst_premium_economy: Optional[float] = None
    gst_business: Optional[float] = None
    gst_first: Optional[float] = None
    reissue_tax_code: Optional[str] = None
    refund_tax_code: Optional[str] = None
    non_refundable_taxes: Optional[str] = None
    market: Optional[str] = None
    
    class Config:
        from_attributes = True