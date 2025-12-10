from sqlalchemy.orm import Session
from schemas import UserCreate,DecodedToken
from models import User
import hashlib
import base64
import os
from datetime import timedelta,datetime
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("FASTAPI_SECRET_KEY")
ALGORITHM = "HS256"
def create_user(user_create :UserCreate,db :Session):
    """新規ユーザーを作成
    
    パスワードをハッシュ化し、ソルトと共にデータベースに保存します。
    
    Args:
        user_create: ユーザー作成情報（username, password）
        db: データベースセッション
        
    Returns:
        User: 作成されたユーザー（パスワードはハッシュ化済み）
    """
    salt = base64.b64encode(os.urandom(32))
    hashed_password = hashlib.pbkdf2_hmac("sha256",user_create.password.encode(),salt,1000).hex()# hmacはバイトのため16進数に変換
    new_user = User(
        # **user_create.model_dump()
        username = user_create.username,
        password = hashed_password,
        salt = salt.decode() #Userデータモデルに列追加
    )
    db.add(new_user)
    db.commit()
    return new_user

def login(username :str,password :str,db :Session):
    """ユーザー認証
    
    ユーザー名とパスワードを検証し、一致すればユーザー情報を返します。
    
    Args:
        username: ユーザー名
        password: パスワード（平文）
        db: データベースセッション
        
    Returns:
        User: 認証成功したユーザー
        None: 認証失敗の場合
    """
    user = db.query(User).filter(User.username==username).first()
    if not user:
        return None
    hashed_password = hashlib.pbkdf2_hmac("sha256",password.encode(),user.salt.encode(),1000).hex()
    if user.password != hashed_password:
        return None
    return user


def create_access_token(username :str,user_id :int,expires_delta :timedelta):
    """JWTアクセストークンを作成
    
    ユーザー情報を暗号化してJWTトークンを生成します。
    
    Args:
        username: ユーザー名
        user_id: ユーザーID
        expires_delta: トークン有効期限
        
    Returns:
        str: 生成されたJWTトークン
    """
    expires = datetime.now() + expires_delta
    payload = {"sub":username,"id":user_id,"exp":expires}
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(token :Annotated[str,Depends(oauth2_scheme)]):
    """現在のユーザー情報を取得
    
    JWTトークンをデコードし、ユーザー情報を検証して返します。
    
    Args:
        token: JWTアクセストークン（Authorizationヘッダーから自動取得）
        
    Returns:
        DecodedToken: デコードされたユーザー情報（username, user_id）

    Raises:
        JWTError:  トークンが不正または期限切れの場合
    """
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username = payload.get("sub")
        user_id = payload.get("id")
        if username is None or user_id is None:
            return None
        return DecodedToken(username=username,user_id=user_id)
    except JWTError:
        raise JWTError