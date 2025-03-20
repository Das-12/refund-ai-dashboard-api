from app.dependencies.auth import (
    required_role, get_company, get_company_by_id, create_company, update_company, delete_company, create_user, get_user_by_id, get_all_user,
    update_user, delete_user
    )
from fastapi import Depends, APIRouter, HTTPException, status, Request, Query
from app.pagination import paginate


router = APIRouter()


@router.get("/super_admin_auth")
async def admin_auth(user_data: dict = Depends(required_role(["super_admin"]))):
    try:
        return {"message": "you are the super admin", "user_data": user_data}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/company_auth")
async def company_auth(user_data: dict = Depends(required_role(["company"]))):
    try:
        return {"message": "you are company", "user_data": user_data}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/staff_auth")
async def staff_auth(user_data: dict = Depends(required_role(["staff"]))):
    try:
        return {"message": "you are staff", "user_data": user_data}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.get("/get_company")
async def get_company_data(request: Request,
                           company_data: dict = Depends(get_company),
                            pagination: bool = True,
                            skip: int = Query(1, alias="skip", ge=1),
                            limit: int = Query(10, alias="limit", ge=1, le=100)):
    try:
        paginated_data = paginate(company_data, skip, limit, request, pagination)
        return paginated_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.get("/get_company/{company_id}")
async def get_company_data_by_id(company_id: int, company_data: dict = Depends(get_company_by_id)):
    try:
        return company_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.post("/create_company")
async def create_company_data(company_data: dict = Depends(create_company)):
    try:
        return company_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.put("/update_company/{company_id}")
async def update_company_data(company_id: int, company_data: dict = Depends(update_company)):
    try:
        return company_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.delete("/delete_company/{company_id}")
async def delete_company_data(company_id: int, company_data: dict = Depends(delete_company)):
    try:
        return company_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.post("/create_user")
async def create_user_data(user_data: dict = Depends(create_user)):
    try:
        return user_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/get_user/{user_id}")
async def get_user_data_by_id(user_id: int, user_data: dict = Depends(get_user_by_id)):
    try:
        return user_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.get("/get_user")
async def get_all_user_data(request: Request,
                            pagination: bool = True,
                            skip: int = Query(1, alias="skip", ge=1),
                            limit: int = Query(10, alias="limit", ge=1, le=100),
                            user_data: dict = Depends(get_all_user)):
    try:
        paginated_data = paginate(user_data, skip, limit, request, pagination)
        return paginated_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.put("/update_user/{user_id}")
async def update_user_data(user_id: int, user_data: dict = Depends(update_user)):
    try:
        return user_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.delete("/delete_user/{user_id}")
async def delete_user_data(user_id: int, user_data: dict = Depends(delete_user)):
    try:
        return user_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
# @router.post("/create_role")
# async def create_role_data(role: dict = Depends(create_role)):
#     return {"message": "role created"}