from typing import Optional
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from utils import OAuth2PasswordBearerWithCookie
import requests

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
#app.mount("/static", StaticFiles(directory="static"), name="static")
OAuth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "xxx@example.com",
        "hashed_password": '$2b$12$k8TH0MdVehAesfP3OeaSwO14wtPqdXq/NYiywZcF4ou8MQ8FggIXS',
        "disabled": False,
        "micro_id": "123"
    }
}


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


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_current_user(token: str = Depends(OAuth2_scheme)):
    credentials_expection = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, "SECRET_KEY123", algorithms="HS256")
        print(f'### token = {token}, payload = {payload}')
        username: str = payload.get("sub")
        if username is None:
            raise credentials_expection
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_expection
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_expection
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "SECRET_KEY123", algorithm="HS256")
    return encoded_jwt


@app.post("/token", response_model=Token)
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(
        fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        samesite="strict"
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get('/todo_auth', response_model=todoUser)
async def todo_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


# todoアプリとのAPIs
@app.post('/todos')
async def get_todos(body: Micro_id):
    header = {'Content-Type': 'application/json'}
    req = await requests.post("http://localhost:5001/user", headers=header, json=body)
    if req.status_code == 200:
        return req
