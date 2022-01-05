from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

    class Config:
        schema_extra = {
            'example': {
                'username': 'johndoe',
                'email': 'johndoe@doe.com',
                'password': 'holamundo' 
            }
        }

class UserModel(UserBase):
    id: int
    is_staff: bool
    is_active: bool

    class Config:
        orm_mode = True


class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    status: Optional[str] = "PENDING"
    pizza_size: Optional[str] = "SMALL"

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 2,
                "pizza_size": "LARGE"
            }
        }

