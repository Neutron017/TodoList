from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from .tags import Tag

class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_done: bool = False

class TaskCreate(TaskBase):
    tag_ids: Optional[List[int]] = None

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None
    tag_ids: Optional[list[int]] = None

class Task(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    tags: List[Tag] = []
    model_config = ConfigDict(from_attributes=True)
