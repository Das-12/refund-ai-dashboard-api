from pydantic import BaseModel
from typing import List, Optional

class RoleBase(BaseModel):
    name: str
    description: str

class RoleCreate(RoleBase):
    pass

class RoleOut(RoleBase):
    id: int

    class Config:
        from_attributes = True
        
class AssignRoleRequest(BaseModel):
    username: str
    role_name: str
    
class AssignRoleOut(BaseModel):
    username: str
    roles: List[str]
    
    class Config:
        from_attributes = True
    
class PermissionOut(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    
    class Config:
        from_attributes = True
    
class MultiRoleOut(BaseModel):
    id: int
    name: str
    description: str
    permissions: Optional[List[PermissionOut]] = None
    
    class Config:
        from_attributes = True