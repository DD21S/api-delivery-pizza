from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    id: Optional[int]
    username: str
    email: str

class UserCreate(UserBase):
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@doe.com",
                "password": "holamundo" 
            }
        }

class UserModel(UserBase):
    is_staff: bool
    is_active: Optional[bool]

class SuperUserCreate(UserModel):
    password: str
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@johndoe.com",
                "password": "admin",
                "is_staff": True
            }
        }


class OrderModel(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    quantity: int
    status: Optional[str]
    pizza_size: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 2,
                "pizza_size": "LARGE"
            }
        }

