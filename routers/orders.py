from fastapi import APIRouter, status

from schemas import OrderModel

orders_router = APIRouter(
    prefix="/orders",
    tags=["order"] 
)

@orders_router.get('/')
async def order():
    return {'message': 'hello world'}

# @orders_router.post(
#     '/',
#     response_model=OrderModel,
#     status_code=status.HTTP_201_CREATED
# )
# async def create_order(
#     current_user
# ):