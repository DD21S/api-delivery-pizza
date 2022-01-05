from fastapi import APIRouter, status, Depends, Path

from typing import List

from sqlalchemy.orm import Session

from schemas import OrderModel, UserModel

from models import Order
import authentication

orders_router = APIRouter(
    prefix="/orders",
    tags=["orders"] 
)

@orders_router.get(
    '/',
    response_model=List[OrderModel],
    status_code=status.HTTP_200_OK
)
async def orders(
    current_user: UserModel = Depends(authentication.get_current_user),
    db: Session = Depends(authentication.get_db)
):
    orders = db.query(Order).filter(current_user.id == Order.user_id).all()

    return orders

@orders_router.post(
    '/',
    response_model=OrderModel,
    status_code=status.HTTP_201_CREATED
)
async def create_order(
    order: OrderModel,
    current_user: UserModel = Depends(authentication.get_current_user),
    db: Session = Depends(authentication.get_db)
):
    new_order = Order(
        quantity=order.quantity,
        pizza_size=order.pizza_size,
        user=current_user
    )

    db.add(new_order)
    db.commit()

    return new_order

@orders_router.put(
    '/{order_id}',
    response_model=OrderModel,
    status_code=status.HTTP_200_OK
)
async def update_order(
    order: OrderModel,
    order_id: int = Path(..., title="The ID of the order to update"),
    current_user: UserModel = Depends(authentication.get_current_user),
    db: Session = Depends(authentication.get_db)
):
    order_update_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You don't have permission to update this order"
    )

    update_order = db.query(Order).filter(Order.id==order_id).first()

    if update_order.id != current_user.id:
        return order_delete_exception

    update_order.quantity = order.quantity
    update_order.pizza_size = order.pizza_size 

    db.commit()

    return update_order

@orders_router.delete(
    '/{order_id}',
    response_model=OrderModel,
    status_code=status.HTTP_200_OK
)
async def delete_order(
    order: OrderModel,
    order_id: int = Path(..., title="The ID of the order to delete"),
    current_user: UserModel = Depends(authentication.get_current_user),
    db: Session = Depends(authentication.get_db)
):  
    order_delete_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You don't have permission to delete this order"
    )

    delete_order = db.query(Order).filter(Order.id==order_id).first()

    if delete_order.id != current_user.id:
        return order_delete_exception

    db.delete(delete_order)
    db.commit()

    return delete_order