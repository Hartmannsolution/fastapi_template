from typing import Optional
from fastapi import FastAPI
from app.api import ping

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# The order matters: the url path of this fixed resource is the same as the below url with path params (so this static one should come first)
@app.get("/items/all")
async def read_user_me(): # async here makes the method superfast asyncronous method. See: https://testdriven.io/blog/fastapi-crud/ for more.
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

# route served from file. api/ping.py by using fastapi.APIRouter
app.include_router(ping.router)