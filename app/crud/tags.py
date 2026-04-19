from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models, schemas

async def get_tags(db: AsyncSession,
                   skip: int = 0,
                   limit: int = 100):
    result = await db.execute(select(models.Tag)
                              .offset(skip)
                              .limit(limit))
    return result.scalars().all()

async def create_tag(db: AsyncSession,
                      tag: schemas.TagCreate):
    db_tag = models.Tag(name=tag.name)
    db.add(db_tag)
    await db.commit()
    await db.refresh(db_tag)
    return db_tag
