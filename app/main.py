from fastapi import FastAPI
from app.db import engine
from app.models import Base
from app.routers import tasks, users

app = FastAPI(title='Task API')

app.include_router(tasks.router)
app.include_router(users.router)


@app.on_event('startup')
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get('/')
async def root():
    return {'message': 'Task API is running'}