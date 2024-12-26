import httpx
from fastapi import Depends, HTTPException, status, Request


AUTH_SERVICE_URL = "http://authentication-service:8000/auth/verify-token"


async def verify_token(request: Request):
    authorization: str = request.headers.get("Authorization")
    apikey: str = request.headers.get("api-key")
    url = str(request.url)
    
    if not authorization or authorization.startswith("Bearee "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid or missing authorization token")
    if not apikey:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid or missing api key")
    
    
    token = authorization.split("Bearer ")[1]
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid or missing token")
    
    
    async with httpx.AsyncClient() as client:
        response = await client.post(AUTH_SERVICE_URL, json={"token": token, "api_key": apikey, "from_url": url})
        
        if response.status_code == 200:
            user_data = response.json()
            return user_data
        
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    
def required_role(required_roles:list[str]):
    
    async def role_permission_dependency(user_data: dict = Depends(verify_token)):
        
        user_role = user_data.get("role")
        if not user_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user role not found")
        
        if user_role not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access forbidden for your role")
        
        return user_data
    return role_permission_dependency
    
        
        
            