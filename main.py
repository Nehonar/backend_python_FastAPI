from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
"""
PRIVATE
"""
from routers import products, users, basic_auth_users, jwt_auth_users

app = FastAPI()

"""
ROUTERS
"""
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)

"""
IMAGES
"""
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/ping")
async def ping():
  return "pong"