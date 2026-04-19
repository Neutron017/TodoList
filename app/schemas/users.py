from pydantic import BaseModel, ConfigDict
from typing import List
from .tasks import Task


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    tasks: List[Task] = []
    model_config = ConfigDict(from_attributes=True)