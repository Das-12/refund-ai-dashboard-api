from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class CurrencyConversionRate(BaseModel):
    id: int
    target_currency: str
    Convertion_rate: float
    created_at: datetime
    base_currency: datetime
    
    class Config:
        from_attributes = True