from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/user",
                   tags=["users"],
                   responses={404: {"message": "Not found"}})

class User(BaseModel):
  id: int
  name: str
  surname: str
  url: str
  age: int

fake_users = [
  User(id=1, name="benit", surname="avila", url="https://linkedin.com/nehonar", age=38),
  User(id=2, name="mireia", surname="plata", url="https://linkedin/mplata", age=36)
  ]

"""
  GET
"""
@router.get("/all_users")
async def users():
  return fake_users

@router.get("/{id}")
async def user(id: int):
  return search_user(id)
  
@router.get("/userquery/")
async def user_query(id: int):
  return search_user(id)

"""
POST
"""
@router.post("/", status_code=201)
async def create_user(user_data: User):
  if type(search_user(user_data.id)) == User:
    raise HTTPException(status_code=204, detail="User already exists.")
  else:
    fake_users.append(user_data)
    return {"response": "OK"}

"""
PUT
"""
@router.put("/")
async def upgrade_user(user_data: User):
  found = False
  for index, user in enumerate(fake_users):
    if user.id == user_data.id:
      fake_users[index] = user_data
      found = True
      return {"response": "OK"}
  if not found:
    return {"error": "User not found"}

"""
DELETE
"""
@router.delete("/{id}")
async def delete_user(id: int):
  found = False
  for index, user in enumerate(fake_users):
    if user.id == id:
      del fake_users[index]
      found = True
      return {"response": "OK"}
  if not found:
    return {"error": "User not found"}

"""
FUNCTIONS
"""
def search_user(id: int):
  users = filter(lambda user: user.id == id, fake_users)

  try:
    return list(users)[0]
  except:
    return {"error": "User not found"}