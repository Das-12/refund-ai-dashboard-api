from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PlanBase(BaseModel):
    name: str
    description: str
    price: int
    max_request: int
    type_of_subscription: str
    additional_price_per_request: int
    
class PlanCreate(PlanBase):
    pass

class PlanUpdate(PlanBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    max_request: Optional[int] = None
    type_of_subscription: Optional[str] = None
    additional_price_per_request: Optional[int] = None

class Plan(PlanBase):
    id: int
    
    class Config:
        from_attributes = True