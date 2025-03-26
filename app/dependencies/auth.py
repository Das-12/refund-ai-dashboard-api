import httpx
from fastapi import Depends, HTTPException, status, Request
import logging
import json
from app.utils import extract_token

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Log to console
        # logging.FileHandler("app.log")  # Uncomment to log to a file
    ]
)

AUTH_SERVICE_URL = "http://authentication-service:8000/auth/verify-token"
GET_COMPANY_URL = "http://authentication-service:8000/auth/get_company"
GET_COMPANY_BY_ID = "http://authentication-service:8000/auth/get_company/{company_id}"
CREATE_COMPANY = "http://authentication-service:8000/auth/register/company"
UPDATED_COMPANY = "http://authentication-service:8000/auth/update_company/{company_id}"
DELETE_COMPANY = "http://authentication-service:8000/auth/delete_company/{company_id}"
CREATE_USER = "http://authentication-service:8000/auth/register/user"
GET_USER_BY_ID = "http://authentication-service:8000/auth/get_user/{user_id}"
GET_ALL_USER = "http://authentication-service:8000/auth/get_all_user"
UPDATE_USER = "http://authentication-service:8000/auth/update_user/{user_id}"
DELETE_USER = "http://authentication-service:8000/auth/delete_user/{user_id}"
GET_USER_BY_COMPANY_ID = "http://authentication-service:8000/auth/get_user_by_company_id/{company_id}"
GET_HEADER_DATA = "http://authentication-service:8000/auth/header_api_first"

async def verify_token(request: Request):
    # print(f"this is request {request}")
    authorization: str = request.headers.get("Authorization")
    apikey: str = request.headers.get("api-key")
    url = str(request.url)
    # print(request.headers)

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing authorization token"
        )
    
    token = authorization.split("Bearer ")[1]
    print(f"this is token before extracting {token}")
    if isinstance(token, str):
        try:
            token = json.loads(token)  # Convert string to a Python object
        except json.JSONDecodeError:
            print("Error: token_request is not valid JSON")
            
    
    if isinstance(token, list):
        if isinstance(token[0], dict) and "access_token" in token[0]:
            token = token[0]["access_token"]
        elif len(token) > 1 and isinstance(token[1], str):
            token = token[1]
    print(f"this is token after extracting {token}")
    # extracted_token = extract_token(token)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )
    async with httpx.AsyncClient() as client:
        response = await client.post(
            AUTH_SERVICE_URL, json={"token": token, "api_key": apikey, "from_url": url}
        )
        print(f"response status code is {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            user_role = user_data.get("role")
            # print(f"This is user data in verify {user_data}")

            if user_role == "super_admin":
                return user_data

            if not apikey:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or missing API key"
                )
            
            return user_data
        else:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
    
    
def required_role(required_roles:list[str]):
    # print("inside required_role")
    async def role_permission_dependency(user_data: dict = Depends(verify_token)):
        
        user_role = user_data.get("role")
        print(f"this is user data {user_role}")
        if not user_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user role not found")
        
        if user_role not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access forbidden for your role")
        
        return user_data
    return role_permission_dependency



async def get_company(request: Request, auth_user: dict = Depends(required_role(["super_admin"]))):
    
    token = request.headers.get("Authorization").split("Bearer ")[1]
    url = str(request.url)
    if auth_user.get("role") != "super_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access forbidden for your role")
    
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get(GET_COMPANY_URL, headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            return user_data
        # print(f"this is response.text {response.text}")
        raise HTTPException(status_code=response.status_code, detail="not authorized")
    
        
async def get_company_by_id(request: Request, company_id: int, auth_user: dict = Depends(required_role(["super_admin"]))):
    
    token = request.headers.get("Authorization").split("Bearer ")[1]
    from_url = str(request.url)
    
    if auth_user.get("role") != "super_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access forbidden for your role")
    
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get(GET_COMPANY_BY_ID.format(company_id=company_id), headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            return user_data
        
        raise HTTPException(status_code=response.status_code, detail=response.text)
        
            
async def create_company(request: Request, company_data: dict, auth_user: dict = Depends(required_role(["super_admin"]))):
    
    token = request.headers.get("Authorization").split("Bearer ")[1]
    
    if auth_user.get("role") != "super_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access forbidden for your role")
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.post(CREATE_COMPANY, json=company_data, headers=headers)
        
        # print(f"this is response status code {response.status_code}")
        # print(f"this is response text {response.text}")
        if response.status_code == 201:
            return response.json()
        else:
            logging.info(f"this is logging response.text {response.text}")
            raise HTTPException(status_code=response.status_code, detail="not authorized")
    

async def update_company(request: Request, company_id: int, company_data: dict, auth_user: dict = Depends(required_role(["super_admin"]))):
    
    token = request.headers.get("Authorization").split("Bearer ")[1]
    
    if auth_user.get("role") != "super_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access forbidden for your role")
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.put(UPDATED_COMPANY.format(company_id=company_id), json=company_data, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        logging.info(f"this is logging response.text {response.text}")
        raise HTTPException(status_code=response.status_code)
    
    
async def delete_company(request: Request, company_id: int, auth_user: dict = Depends(required_role(["super_admin"]))):
    
    token = request.headers.get("Authorization").split("Bearer ")[1]
    
    if auth_user.get("role") != "super_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access forbidden for your role")
    
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.delete(DELETE_COMPANY.format(company_id=company_id), headers=headers)
        
        if response.status_code == 200:
            return response.json()
        logging.info(f"this is logging response.text {response.text}")
        raise HTTPException(status_code=response.status_code)
    
    
async def create_user(request: Request, user_data: dict, auth_user: dict = Depends(required_role(["super_admin", "company"]))):
    print("inside create_user dependency")
    token = request.headers.get("Authorization").split("Bearer ")[1]
    
    if auth_user.get("role") == "super_admin" or auth_user.get("role") == "company":
        print(f"this is userrole {auth_user.get("role")}")
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.post(CREATE_USER, json=user_data, headers=headers)
            print(f"response status code is {response.status_code}")
            if response.status_code == 201:
                return response.json()
            logging.info(f"this is logging response.text {response.text}")
            raise HTTPException(status_code=response.status_code, detail=response.text)
    else:    
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access forbidden for your role")
    

async def get_user_by_id(request: Request, user_id: int, auth_user: dict = Depends(required_role(["super_admin", "company"]))):
    
    token = request.headers.get("Authorization").split("Bearer ")[1]
    
    if auth_user.get("role") == "super_admin" or auth_user.get("role") == "company":
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(GET_USER_BY_ID.format(user_id=user_id), headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                return user_data
            raise HTTPException(status_code=response.status_code)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access forbidden for your role")
    
    
async def get_user_by_company_id(request: Request, company_id: int, auth_user: dict = Depends(required_role(["super_admin", "company"]))):
    
    token = request.headers.get("Authorization").split("Bearer ")[1]
    
    if auth_user.get("role") == "super_admin" or auth_user.get("role") == "company":
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(GET_USER_BY_COMPANY_ID.format(company_id=company_id), headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                return user_data
            raise HTTPException(status_code=response.status_code)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access forbidden for your role")


async def get_all_user(request: Request, auth_user: dict = Depends(required_role(["super_admin", "company"]))):
    token = request.headers.get("Authorization").split("Bearer ")[1]
    
    if auth_user.get("role") == "super_admin" or auth_user.get("role") == "company":
    
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(GET_ALL_USER, headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                return user_data
            raise HTTPException(status_code=response.status_code, detail=response.text)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access forbidden for your role")

async def update_user(request: Request, user_id: int, user_data: dict, auth_user: dict = Depends(required_role(["super_admin", "company"]))):
    
    token = request.headers.get("Authorization").split("Bearer ")[1]
    
    if auth_user.get("role") == "super_admin" or auth_user.get("role") == "company":
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.put(UPDATE_USER.format(user_id = user_id), json=user_data, headers=headers)
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=response.status_code)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access forbidden for your role")
    
    
async def delete_user(request: Request, user_id: int, auth_user: dict = Depends(required_role(["super_admin", "company"]))):
    
    token = request.headers.get("Authorization").split("Bearer ")[1]
    
    if auth_user.get("role") == "super_admin" or auth_user.get("role") == "company":
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.delete(DELETE_USER.format(user_id=user_id), headers=headers)
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=response.status_code, detail=response.text)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access forbidden for your role")

    
async def get_header_data(request: Request, auth_user: dict = Depends(required_role(["super_admin"]))):
    token = request.headers.get("Authorization").split("Bearer ")[1]
    
    if auth_user.get("role") == "super_admin":
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(GET_HEADER_DATA, headers=headers)
            print(f"this is response status code in dash {response.status_code}")
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=response.status_code, detail=response.text)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access forbidden for your role")