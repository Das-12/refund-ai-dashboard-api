from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class SubscriptionBase(BaseModel):
    company_id: int
    plan_id: int
    start_date: Optional[date] = None

class SubscriptionCreate(SubscriptionBase):
    pass
    class Config:
        from_attributes = True

class SubscriptionUpdate(BaseModel):
    company_id: Optional[int] = None
    plan_id: Optional[int] = None
    start_date: Optional[datetime] = None

class SubscriptionResponse(SubscriptionBase):
    id: int
    end_date: date
    
    class Config:
        from_attributes = True