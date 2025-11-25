from fastapi import APIRouter,Depends,HTTPException
from schemas import UserResponse,UserCreate
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from cruds import auth as auth_cruds
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter(prefix="/auth",tags=["auth"])
DbDependency = Annotated[Session,Depends(get_db)]
FormDependency = Annotated[OAuth2PasswordRequestForm,Depends()]

@router.post("/signup",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def create_user(user_create :UserCreate,db :DbDependency):
    return auth_cruds.create_user(user_create,db)

@router.post("/login")
async def login(db :DbDependency,form_data :FormDependency):
    user = auth_cruds.login(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=401,detail="Incorrect username or password")
    token = auth_cruds.create_access_token(user.username,user.id,timedelta(minutes=20))
    return {"access_token":token,"token_type":"bearer"}