from pydantic import BaseModel, ConfigDict
from typing import Optional


class TagsBase(BaseModel):
    name: str

class TagsCreate(TagsBase):
    pass

class TagsUpdate(BaseModel):
    username: Optional[str] = None

class Tags(TagsBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
