from sqlalchemy.orm import Session
from schemas import UserCreate
from models import User
import hashlib
import base64
import os

def create_user(user_create :UserCreate,db :Session):
    salt = base64.b64encode(os.random(32))
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