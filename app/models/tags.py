from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.tasks import Task
    from app.models.task_tag import TaskTag

class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    task_tags: Mapped[List['TaskTag']] = relationship(
        back_populates='tag', cascade="all, delete-orphan"
    )

    tasks: Mapped[List['Task']] = relationship(
        secondary='task_tag', back_populates='tags', viewonly=True
    )