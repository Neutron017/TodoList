from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from .tasks import Task


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    tasks: List[Task] = []
    model_config = ConfigDict(from_attributes=True)