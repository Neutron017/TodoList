from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.tasks import Task
    from app.models.tags import Tag

class TaskTag(Base):
    __tablename__ = 'task_tag'

    task_id: Mapped[int] = mapped_column(
        ForeignKey('tasks.id', ondelete='CASCADE'), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True
    )

    task: Mapped['Task'] = relationship(back_populates='task_tags')
    tag: Mapped['Tag'] = relationship(back_populates='task_tags')