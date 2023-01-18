from fastapi import Depends, FastAPI
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_async_session
from database.models import post
from database.schemas import CorrectPost

app = FastAPI(
    title='Posting App'
)

@app.get('/posts/')
async def get_all_posts(session: AsyncSession = Depends(get_async_session)):
    query = select(post)
    result = await session.execute(query)

    return result.all()
    

@app.get('/posts/{post_id}')
async def get_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(post).where(post.c.id == post_id)
    result = await session.execute(query)
    our_post = result.first()
    if our_post:
        return our_post
    return f'post with id: {post_id} not found'

@app.delete('/posts/{post_id}')
async def delete_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(post).where(post.c.id == post_id)
    await session.execute(stmt)
    await session.commit()

    return {'status': 200}

    

@app.post('/posts/create')
async def add_post(new_post: CorrectPost, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(post).values(**new_post.dict())
    await session.execute(stmt)
    await session.commit()

    return {'status': 200}