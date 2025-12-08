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
    """新規ユーザー登録
    
    ユーザー名とパスワードで新しいアカウントを作成します。
    
    Returns:
        UserResponse: 作成されたユーザー情報（id, username）
    """
    return auth_cruds.create_user(user_create,db)

@router.post("/login")
async def login(db :DbDependency,form_data :FormDependency):
    """ログイン
    
    ユーザー名とパスワードで認証し、JWTトークンを取得します。
    取得したトークンは以降のAPI呼び出しで使用します。
    
    Returns:
        dict: アクセストークン(JWT)、トークンタイプ
    Raise:
        HTTPException: 認証失敗（401）
    """
    user = auth_cruds.login(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=401,detail="Incorrect username or password")
    token = auth_cruds.create_access_token(user.username,user.id,timedelta(minutes=20))
    return {"access_token":token,"token_type":"bearer"}

