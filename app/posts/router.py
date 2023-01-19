from fastapi import APIRouter, Depends
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_async_session
from app.database.models import post
from app.database.schemas import CorrectPost

router = APIRouter(
    prefix='/posts',
    tags=['post']
)

@router.get('/')
async def get_all_posts(session: AsyncSession = Depends(get_async_session)):
    query = select(post)
    result = await session.execute(query)

    return result.all()
    
@router.get('/{post_id}')
async def get_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(post).where(post.c.id == post_id)
    result = await session.execute(query)
    our_post = result.first()
    if our_post:
        return our_post
    return f'post with id: {post_id} not found'

@router.delete('/{post_id}')
async def delete_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(post).where(post.c.id == post_id)
    await session.execute(stmt)
    await session.commit()

    return {'status': 200}

@router.post('/create')
async def add_post(new_post: CorrectPost, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(post).values(**new_post.dict())
    await session.execute(stmt)
    await session.commit()

    return {'status': 200}