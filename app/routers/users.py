from fastapi import APIRouter, Depends, HTTPException, status
from pydantic.v1 import NoneIsAllowedError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app import crud, schemas
from app.db import get_db

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/', response_model=List[schemas.User])
async def read_users(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db),
):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post('/', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(
        user: schemas.UserCreate,
        db: AsyncSession = Depends(get_db)
):
    db_user = await crud.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username already registered'
        )
    return await crud.create_user(db=db, user=user)


@router.get('/{user_id}', response_model=schemas.User)
async def read_user(
        user_id: int,
        db: AsyncSession = Depends(get_db)
):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return db_user


@router.put('/{user_id}', response_model=schemas.User)
async def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    db_user = await crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return db_user


@router.delete('/{user_id}', response_model=schemas.User)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_user = await crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found')
    return db_user
