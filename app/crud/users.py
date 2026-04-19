from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app import models, schemas


async def get_user(
        db: AsyncSession,
        user_id: int):
    result = await db.execute(
        select(models.User)
        .options(selectinload(models.User.tasks)
                 .selectinload(models.Task.tags))
        .where(models.User.id == user_id)
    )
    return result.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession,
                               username: str):
    result = await db.execute(select(models.User)
                              .where(models.User.username == username))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession,
                      user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    await db.refresh(db_user, attribute_names=['tasks'])
    return db_user
