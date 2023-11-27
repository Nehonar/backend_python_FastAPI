from fastapi import APIRouter, HTTPException, status
from models.user import User
from db.client import db_client
from schemas.user import user_schema, users_schema

router = APIRouter(prefix="/user",
                   tags=["users"],
                   responses={
                     status.HTTP_404_NOT_FOUND: {"message": "Not found"}
                     })

users_list = []

"""
  GET
"""
@router.get("/", response_model=list(User))
async def users():
  return users_schema(db_client.local.users.find())

@router.get("/{id}")
async def user(id: int):
  return search_user(id)
  
@router.get("/")
async def user_query(id: int):
  return search_user(id)

"""
POST
"""
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
  if type(search_user_by_email(user.email)) == User:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="User already exists."
      )
    
  user_dict = dict(user)
  del user_dict["id"]
  
  id = db_client.local.users.insert_one(user_dict).inserted_id
  new_user = user_schema(db_client.local.users.find_one({"_id": id}))
  
  return User(**new_user)

"""
PUT
"""
@router.put("/")
async def upgrade_user(user_data: User):
  found = False
  for index, user in enumerate(users_list):
    if user.id == user_data.id:
      users_list[index] = user_data
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
  for index, user in enumerate(users_list):
    if user.id == id:
      del users_list[index]
      found = True
      return {"response": "OK"}
  if not found:
    return {"error": "User not found"}

"""
FUNCTIONS
"""
def search_user_by_email(email: str):
  try:
    user = db_client.local.users.find_one({"email": email})
    return User(**user_schema(user))
  except:
    return {"error": "User not found"}