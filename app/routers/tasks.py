from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import crud, schemas
from app.db import get_db


router = APIRouter(prefix='/tasks', tags=['tasks'])

@router.get('/', response_model=List[schemas.Task])
async def read_tasks(skip: int = 0,
                     limit: int = 0,
                     db: AsyncSession = Depends(get_db)):
    tasks = await crud.get_tasks(db, skip=skip, limit=limit)
    return tasks

@router.post('/', response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate,
                      db: AsyncSession = Depends(get_db)):
    user_id = 1
    result = await crud.create_task(db=db, task=task, user_id=user_id)
    return result

@router.get('/{task_id}', response_model=schemas.Task)
async def read_task(task_id: int,
                    db: AsyncSession = Depends(get_db)):
    db_task = await crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return db_task

@router.put('/{task_id}', response_model=schemas.Task)
async def read_task(task_id: int,
                    task: schemas.TaskUpdate,
                    db: AsyncSession = Depends(get_db)):
    db_task = await crud.update_task(db, task_id=task_id, task_update=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return db_task


@router.delete('/{task_id}', response_model=schemas.Task)
async def read_task(task_id: int,
                    db: AsyncSession = Depends(get_db)):
    db_task = await crud.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return db_task
