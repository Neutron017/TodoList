from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app import models, schemas


async def get_tasks(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10
):
    result = await db.execute(
        select(models.Task)
        .options(selectinload(models.Task.tags))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_task(
        db: AsyncSession,
        task_id: int
):
    result = await db.execute(
        select(models.Task)
        .options(selectinload(models.Task.tags))
        .where(models.Task.id == task_id)
    )
    return result.scalar_one_or_none()

async def create_task(
        db: AsyncSession,
        task: schemas.TaskCreate,
        user_id: int
):
    db_task = models.Task(
        user_id=user_id,
        name=task.name,
        description=task.description,
        is_done=task.is_done
    )
    if task.tag_ids:
        tag = await db.execute(
            select(models.Tag).where(models.Tag.id.in_(task.tag_ids))
        )
        db_task.tags = tag.scalars().all()
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task, attribute_names=['tags'])
    return db_task

async def update_task(db: AsyncSession,
                      task_update: schemas.TaskUpdate,
                      task_id: int):
    db_task = await get_task(db, task_id)
    if not db_task:
        return None
    update_data = task_update.model_dump(exclude_unset=True)
    tag_ids = update_data.pop('tag_ids', None)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    if tag_ids is not None:
        tag_result = await db.execute(select(models.Tag).where(models.Tag.id.in_(tag_ids)))
        db_task.tags = tag_result.scalars().all()
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def delete_task(db: AsyncSession,
                      task_id: int):
    db_task = await get_task(db, task_id)
    if db_task:
        await db.delete(db_task)
        await db.commit()
    return db_task

