from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   tags=["products"],
                   responses={404: {"message": "Not found"}})

fake_products = ["products 1", "products 2", "products 3", "products 4"]

@router.get("/")
async def products():
  return fake_products

@router.get("/{id}")
async def products(id: int):
  return fake_products[id]