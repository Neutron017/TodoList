from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app import models, schemas



async def get_users(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
):
    result = await db.execute(
        select(models.User)
        .options(selectinload(models.User.tasks)
                 .selectinload(models.Task.tags))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

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

async def create_user(
        db: AsyncSession,
        user: schemas.UserCreate
):
    db_user = models.User(
        username=user.username,
        password=user.password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user, attribute_names=['tasks'])
    return db_user


async def update_user(
        db: AsyncSession,
        user_id : int,
        user_update: schemas.UserUpdate
):
    db_user = await get_user(db, user_id)
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(
        db: AsyncSession,
        user_id: int
):
    db_user = await get_user(db, user_id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
    return db_user
