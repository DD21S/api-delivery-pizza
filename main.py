from fastapi import FastAPI

from routers.auth import auth_router
from routers.orders import orders_router

from database import engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(orders_router)