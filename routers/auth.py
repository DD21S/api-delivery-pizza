from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from models import User
from schemas import UserCreate, UserModel, SuperUserCreate

import authentication

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"] 
)

@auth_router.post(
    '/signup', 
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED
)
async def signup(
    user: UserCreate,
    db: Session = Depends(authentication.get_db)
):
    user_create_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User with this username or email already exists"
    )

    db_username = db.query(User).filter(User.username==user.username).first()
    db_email = db.query(User).filter(User.email==user.email).first()

    if db_username is not None:
        raise user_create_exception

    elif db_email is not None:
        raise user_create_exception

    new_user = User(
        username=user.username,
        email=user.email,
        password=authentication.get_password_hash(user.password)
    )

    db.add(new_user)
    db.commit()

    return new_user

@auth_router.post(
    '/createsuperuser', 
    status_code=status.HTTP_201_CREATED
)
async def createsuperuser(
    user: SuperUserCreate,
    secret_key: str,
    db: Session = Depends(authentication.get_db)
):
    user_create_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User with this username or email already exists"
    )

    db_username = db.query(User).filter(User.username==user.username).first()
    db_email = db.query(User).filter(User.email==user.email).first()

    if db_username is not None:
        raise user_create_exception

    elif db_email is not None:
        raise user_create_exception

    elif secret_key != authentication.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="secret_key incorrect"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=authentication.get_password_hash(user.password),
        is_staff=True
    )

    db.add(new_user)
    db.commit()

    return jsonable_encoder({
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "is_staff": new_user.is_staff 
    })

@auth_router.post(
    "/login",
    response_model=authentication.Token,
    status_code=status.HTTP_200_OK
)
async def login(
    db: Session = Depends(authentication.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authentication.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=authentication.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = authentication.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}