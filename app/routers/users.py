from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.db import get_db


router = APIRouter(prefix='/users', tags=['users'])




@router.post('/', response_model=schemas.User)
async def create_user(user: schemas.UserCreate,
                      db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_username(db=db, username=user.username)
    print(db_user, user.username)
    if db_user:
        raise HTTPException(status_code=404, detail='Username already registered')

    return await crud.create_user(db=db, user=user)

@router.get('/{user_id}', response_model=schemas.User)
async def read_task(user_id: int,
                    db: AsyncSession = Depends(get_db)):
    db_task = await crud.get_user(db, user_id=user_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_task
