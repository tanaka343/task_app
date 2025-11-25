from fastapi import APIRouter,Depends
from schemas import UserResponse,UserCreate
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from cruds import auth as auth_cruds

router = APIRouter(prefix="/auth",tags=["auth"])
DbDependency = Annotated[Session,Depends(get_db)]

@router.post("/signup",response_model=UserResponse)
async def create_user(user_create :UserCreate,db :DbDependency):
    return auth_cruds.create_user(user_create,db)