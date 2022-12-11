from pydantic import BaseModel
from typing import Optional


class AccessToken(BaseModel):
    access_token: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    micro_id: str


class todoUser(BaseModel):
    micro_id: str
    username: str


class UserInDB(User):
    hashed_password: str


class Micro_id(BaseModel):
    micro_id: str
