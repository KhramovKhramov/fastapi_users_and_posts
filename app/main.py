from fastapi import Depends, FastAPI
from fastapi_users import FastAPIUsers
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead
from database.db import User, get_async_session
from database.models import post
from database.schemas import CorrectPost

app = FastAPI(
    title='Posting App'
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
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