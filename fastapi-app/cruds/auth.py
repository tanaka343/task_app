from sqlalchemy.orm import Session
from schemas import UserCreate
from models import User
import hashlib
import base64
import os
from datetime import timedelta,datetime
from jose import jwt


def create_user(user_create :UserCreate,db :Session):
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
    user = db.query(User).filter(User.username==username).first()
    if not user:
        return None
    hashed_password = hashlib.pbkdf2_hmac("sha256",password.encode(),user.salt.encode(),1000).hex()
    if user.password != hashed_password:
        return None
    return user

SECRET_KEY = "91828183e516b1314a1efd282d875320e64fafb2356e23a456d32a600a495d6c"
ALGORITHM = "HS256"
def create_access_token(username :str,user_id :int,expires_delta :timedelta):
    expires = datetime.now() + expires_delta
    payload = {"sub":username,"id":user_id,"exp":expires}
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)