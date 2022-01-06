from fastapi import APIRouter, status, Depends, Path, HTTPException
from fastapi.encoders import jsonable_encoder

from typing import List

from sqlalchemy.orm import Session

from schemas import OrderModel, UserModel

from models import Order, User
import authentication

def get_order_to_json(order):
    json_order = {
        "id": order.id,
        "quantity": order.quantity,
        "status": order.status,
        "pizza_size": order.pizza_size
    }

    return json_order

def get_max_id(db):
    return db.query(Order).all()[-1].id

orders_router = APIRouter(
    prefix="/orders",
    tags=["orders"] 
)

@orders_router.get(
    '',
    status_code=status.HTTP_200_OK
)
async def orders(
    current_user: UserModel = Depends(authentication.get_current_user),
    db: Session = Depends(authentication.get_db)
):
    orders = db.query(Order).filter(current_user.id == Order.user_id).all()

    return jsonable_encoder(orders)

@orders_router.post(
    '',
    status_code=status.HTTP_201_CREATED
)
async def create_order(
    order: OrderModel,
    current_user: UserModel = Depends(authentication.get_current_user),
    db: Session = Depends(authentication.get_db)
):  
    user = db.query(User).filter(User.id==current_user.id).first()

    new_order = Order(
        quantity=order.quantity,
        pizza_size=order.pizza_size,
    )

    new_order.user = user

    db.add(new_order)
    db.commit()

    return jsonable_encoder(get_order_to_json(new_order))

@orders_router.put(
    '/{order_id}',
    status_code=status.HTTP_200_OK
)
async def update_order(
    order: OrderModel,
    order_id: int = Path(..., title="The ID of the order to update"),
    current_user: UserModel = Depends(authentication.get_current_user),
    db: Session = Depends(authentication.get_db)
):
    if order_id > get_max_id(db):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )

    order_update_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You don't have permission to update this order"
    )

    update_order = db.query(Order).filter(Order.id==order_id).first()

    if update_order.user_id != current_user.id:
        return order_update_exception

    update_order.quantity = order.quantity
    update_order.pizza_size = order.pizza_size 

    db.commit()

    return jsonable_encoder(get_order_to_json(update_order))

@orders_router.delete(
    '/{order_id}',
    status_code=status.HTTP_200_OK
)
async def delete_order(
    order_id: int = Path(..., title="The ID of the order to delete"),
    current_user: UserModel = Depends(authentication.get_current_user),
    db: Session = Depends(authentication.get_db)
):  
    if order_id > get_max_id(db):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )    

    order_delete_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You don't have permission to delete this order"
    )

    delete_order = db.query(Order).filter(Order.id==order_id).first()

    if delete_order.user_id != current_user.id:
        return order_delete_exception

    db.delete(delete_order)
    db.commit()

    return jsonable_encoder(get_order_to_json(delete_order))