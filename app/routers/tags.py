from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app import crud, schemas
from app.db import get_db

router = APIRouter(prefix='/tags', tags=['tags'])


@router.get('/', response_model=List[schemas.Tags])
async def read_tags(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    tags = await crud.get_tags(db, skip=skip, limit=limit)
    return tags

@router.post('/', response_model=schemas.Tags, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag: schemas.TagsCreate,
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_tag(db=db, tag=tag)

@router.get('/{tag_id}', response_model=schemas.Tags)
async def read_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_tag = await crud.get_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tag not found'
        )
    return db_tag


@router.put('/{tag_id}', response_model=schemas.Tags)
async def update_tag(
    tag_id: int,
    tag_update: schemas.TagsUpdate,
    db: AsyncSession = Depends(get_db)
):
    db_tag = await crud.update_tag(db, tag_id=tag_id, tag_update=tag_update)
    if db_tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tag not found'
        )
    return db_tag


@router.delete('/{tag_id}', response_model=schemas.Tags)
async def delete_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_tag = await crud.delete_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tag not found'
        )
    return db_tag
