from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "473a130d7d13c9e8e21971bc1534bbf465b0277bdbe6ccbe9da53f24e049506d"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
  username: str
  full_name: str
  email: str
  disabled: bool

class UserDB(User):
  password: str

users_db = {
  "Nehonar": {
    "username": "Nehonar",
    "full_name": "Benito Avila",
    "email": "benito.avar@gmail.com",
    "disabled": False,
    "password": "$2a$12$kv9pk/eInaox/Yfeuqdpm.1Nk6YJJbT6cOl4AlD.5DmD6JdTTCcAu"
  },
  "Nehonar2": {
    "username": "Nehonar2",
    "full_name": "Benito Avila",
    "email": "nehonar@gmail.com",
    "disabled": True,
    "password": "$2a$12$jpmkd2JydSX0d8YFzX1bIeWsZgIU4b958sMigvWLT8CFSkIEtFNC."
  }
}

def search_user_db(username: str):
  if username in users_db:
    return UserDB(**users_db[username])
  
def search_user(username: str):
  if username in users_db:
    return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
  exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"}
    )
  
  try:
    username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
    if username is None:
      raise exception
  except JWTError:
    raise exception
  
  return search_user(username)


async def current_user(user: User = Depends(auth_user)):
  if user.disabled:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Inactive user"
    )
  
  return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
  user_db = users_db.get(form.username)
  
  if not user_db:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, 
      detail="Incorrect user"
      )
  
  user = search_user_db(form.username)

  if not crypt.verify(form.password, user.password):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, 
      detail="Incorrect password"
      )
  
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

  access_token = {
    "sub": user.username,
    "exp": expire
  }

  resposne = {
    "access_token": jwt.encode(
      access_token, 
      SECRET, 
      algorithm=ALGORITHM
    ), 
    "token_type": "bearer"
  }
  return resposne

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
  return user