from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SubscriptionBase(BaseModel):
    company_id: int
    plan_id: int
    start_date: Optional[datetime] = None

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    company_id: Optional[int] = None
    plan_id: Optional[int] = None
    start_date: Optional[datetime] = None

class SubscriptionResponse(SubscriptionBase):
    id: int
    end_date: datetime
    
    class Config:
        from_attributes = True