# pydantic models to use for type checking.
from typing import  Optional
from pydantic import BaseModel

# Item
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int
    class Config: # class is used to provide configurations to Pydantic Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
        orm_mode = True

# User
class UserBase(BaseModel):
    email: str

# Extend the base entity with a password to use when first creating a user.
class UserCreate(UserBase):
    password: str

# Extend the user for DTO purpose of representing a user.
class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = [] # valid from python 3.9
    class Config:
        orm_mode = True
