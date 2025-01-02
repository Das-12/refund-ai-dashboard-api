from app.dependencies.auth import required_role, get_company, get_company_by_id, create_company, update_company, delete_company
from fastapi import Depends, APIRouter


router = APIRouter()


@router.get("/super_admin_auth")
async def admin_auth(user_data: dict = Depends(required_role(["admin"]))):
    return {"message": "you are the super admin", "user_data": user_data}


@router.get("/company_auth")
async def company_auth(user_data: dict = Depends(required_role(["company"]))):
    return {"message": "you are company", "user_data": user_data}


@router.get("/staff_auth")
async def staff_auth(user_data: dict = Depends(required_role(["staff"]))):
    return {"message": "you are staff", "user_data": user_data}

@router.get("/get_company")
async def get_company_data(company_data: dict = Depends(get_company)):
    return company_data

@router.get("/get_company/{company_id}")
async def get_company_data_by_id(company_id: int, company_data: dict = Depends(get_company_by_id)):
    return company_data

@router.post("/create_company")
async def create_company_data(company_data: dict = Depends(create_company)):
    return company_data

@router.put("/update_company/{company_id}")
async def update_company_data(company_id: int, company_data: dict = Depends(update_company)):
    return company_data

@router.delete("/delete_company/{company_id}")
async def delete_company_data(company_id: int, company_data: dict = Depends(delete_company)):
    return company_data