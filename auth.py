from os import access
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate(name: str, password: str):
  """パスワード認証し、userを返却"""
  user = User.get(name=name)
  if user.password != password:
    raise HTTPException(status_code=401, detail="パスワード不一致")
  return user

def create_tokens(user_id: int):
  """パスワード認証を行い、tokenを生成する"""
  access_payload = {
    "token_type": "access_token",
    "exp": datetime.utcnow() + timedelta(minutes=60),
    "user_id": user_id
  }
  refresh_payload = {
    "token_type": "refresh_token",
    "exp": datetime.utcnow() + timedelta(days=90),
    "user_id": user_id
  }

  # token作成
  access_token = jwt.encode(access_payload, "SECRET_KEY123", algorithm="HS256")
  refresh_token = jwt.encode(refresh_payload, "SECRET_KEY123", algorithm="HS256")

  # DBにリフレッシュtokenを保存
  User.update(refresh_token=refresh_token).where(User.id == user_id).execute()

  return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

def get_current_user_from_token(token: str, token_type: str):
  """tokenからユーザを取得"""
  # トークンをデコードしてpayloadを取得。有効期限と署名は自動で検証される。
  payload = jwt.decode(token, "SECRET_KEY123", algorithms=["HS256"])

  if payload["token_type"] != token_type:
    raise HTTPException(status_code=401, detail=f"トークンtype不一致")
  
  user = User.get_by_id(payload["user_id"])

  if token_type == "refresh_token" and user.refresh_token != token:
    print(user.refresh_token, token)
    raise HTTPException(status_code=401, detail="リフレッシュtoken不一致")
  
  return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
  """アクセストークンからログイン中のユーザを取得"""
  return get_current_user_from_token(token, "access_token")

async def get_current_user_with_refresh_token(token: str = Depends(oauth2_scheme)):
  return get_current_user_from_token(token, "refresh_token")
  