from fastapi import APIRouter, status, Depends, Path, HTTPException, Body
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from schemas import UserModel

from models import Order
import authentication

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"] 
)

no_staff_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="You are not staff user"
)

@admin_router.get(
    '/orders',
    status_code=status.HTTP_200_OK
)
async def orders(
    current_user: UserModel = Depends(authentication.get_current_user),
    db: Session = Depends(authentication.get_db)
):
    if not current_user.is_staff:
        return no_staff_exception

    orders = db.query(Order).all()

    return jsonable_encoder(orders)

@admin_router.patch(
    '/orders/{order_id}',
    status_code=status.HTTP_200_OK
)
async def update_order(
    status: str = Body(...),
    order_id: int = Path(..., title="The ID of the order to update"),
    current_user: UserModel = Depends(authentication.get_current_user),
    db: Session = Depends(authentication.get_db)
):
    if not current_user.is_staff:
        return no_staff_exception

    update_order = db.query(Order).filter(Order.id==order_id).first()
    update_order.status = status

    db.commit()

    return jsonable_encoder(update_order)

@admin_router.delete(
    '/orders/{order_id}',
    status_code=status.HTTP_200_OK
)
async def delete_order(
    order_id: int = Path(..., title="The ID of the order to delete"),
    current_user: UserModel = Depends(authentication.get_current_user),
    db: Session = Depends(authentication.get_db)
):  
    if not current_user.is_staff:
        return no_staff_exception

    delete_order = db.query(Order).filter(Order.id==order_id).first()

    db.delete(delete_order)
    db.commit()

    return jsonable_encoder(delete_order)