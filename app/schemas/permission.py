from pydantic import BaseModel
from typing import Optional, List

class permissionBase(BaseModel):
    name: str
    description: str
    
class permissionCreate(permissionBase):
    pass

class permissionOut(permissionBase):
    id: int
    
    class Config:
        from_attributes = True
        
class AssignPermissionRequest(BaseModel):
    role_name: str
    permission_name: str
    
class AssignPermissionsOut(BaseModel):
    username: str
    permissions: List[str]
    
    class Config:
        from_attributes = True
        
class AssignPermissionResponse(BaseModel):
    role: str
    permissions: List[str]

    class Config:
        from_attributes = True