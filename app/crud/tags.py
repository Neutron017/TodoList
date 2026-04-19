from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models, schemas

async def get_tags(db: AsyncSession,
                   skip: int = 0,
                   limit: int = 10):
    result = await db.execute(
        select(models.Tag)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_tag(
        db: AsyncSession,
        tag_id: int
):
    result = await db.execute(
        select(models.Tag).where(models.Tag.id == tag_id)
    )
    return result.scalar_one_or_none()

async def create_tag(
        db: AsyncSession,
        tag: schemas.TagsCreate
):
    db_tag = models.Tag(name=tag.name)
    db.add(db_tag)
    await db.commit()
    await db.refresh(db_tag)
    return db_tag

async def update_tag(
        db: AsyncSession,
        tag_id: int,
        tag_update: schemas.TagsUpdate
):
    db_tag = await get_tag(db, tag_id)
    if not db_tag:
        return None

    update_data = tag_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tag, field, value)

    await db.commit()
    await db.refresh(db_tag)
    return db_tag

async def delete_tag(
        db: AsyncSession,
        tag_id: int
):
    db_tag = await get_tag(db, tag_id)
    if db_tag:
        await db.delete(db_tag)
        await db.commit()
    return db_tag
