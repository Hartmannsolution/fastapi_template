from typing import Optional
from fastapi import  Depends, FastAPI, HTTPException
from app.api import ping
from . import facade, models, schemas
from .db import SessionLocal, engine
from sqlalchemy.orm import Session

# from app.db import engine, database, metadata

app = FastAPI()
models.Base.metadata.create_all(bind=engine) # creates all tables that extends the Base class.
# # For the database.
# @app.on_event("startup")
# async def startup():
#     await database.connect()

# # For the database.
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# The order matters: the url path of this fixed resource is the same as the below url with path params (so this static one should come first)
@app.get("/items/all")
async def read_user_me(): # async here makes the method superfast asyncronous method. See: https://testdriven.io/blog/fastapi-facade/ for more.
    return {"all": "show all the items here ..."}

# Path params
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None): # Type declaration here will ensure that item_id will be parsed as an int and a nicely formatted error message is returned if we try to put text in the parameter on the url request.
    return {"item_id": item_id, "q": q}

# Using enums for parameters makes the documentation show legitimate options
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    print(model_name)
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!!!!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# FROM OTHER FILES: route served from file. api/ping.py by using fastapi.APIRouter
app.include_router(ping.router)

# USING ORM WITH SQLALCHEMY
# Dependency: We need to have an independent database session/connection (SessionLocal) per request, use the same session through all the request and then close it after the request is finished.
def get_db():
    db = SessionLocal() # SessionLocal from db module contains the sqlalchemy engine.
    try:
        yield db
    finally:
        db.close()

# These methods can not use async (since it is not supported by sqlalchemy)
# CREATE
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = facade.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return facade.create_user(db=db, user=user)

# READ ALL
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = facade.get_users(db, skip=skip, limit=limit)
    return users

# READ BY ID
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = facade.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# CREATE ITEM ON USER
@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return facade.create_user_item(db=db, item=item, user_id=user_id)

# READ ALL
@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = facade.get_items(db, skip=skip, limit=limit)
    return items
