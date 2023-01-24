from fastapi import APIRouter, Depends
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_async_session
from app.database.models import post
from app.database.schemas import CorrectPost
from fastapi.exceptions import HTTPException

router = APIRouter(
    prefix='/posts',
    tags=['post']
)

@router.get('/')
async def get_all_posts(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(post)
        result = await session.execute(query)

        return {
            "status": "success",
            "data": result.all(),
            "details": None
            }
    except:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Неизвестная ошибка"
        })
    
@router.get('/{post_id}')
async def get_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(post).where(post.c.id == post_id)
        result = await session.execute(query)
        our_post = result.first()
        if our_post:
            return {
                "status": "success",
                "data": our_post,
                "details": None
                }
        else: 
            return {
                "status": "error",
                "data": None,
                "details": f"Пост с id {post_id} не найден"
                }
    except:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Неизвестная ошибка"
        })
    

@router.delete('/{post_id}')
async def delete_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = select(post).where(post.c.id == post_id)
        await session.execute(stmt)
        await session.commit()

        return {
            "status": "success",
            "data": None,
            "details": "Пост удален"
        }
    except:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Неизвестная ошибка"
        })

@router.post('/create')
async def add_post(new_post: CorrectPost, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(post).values(**new_post.dict())
        await session.execute(stmt)
        await session.commit()

        return {
            "status": "success",
            "data": new_post,
            "details": "Пост создан"
        }
    except:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Неизвестная ошибка"
        })

@router.post('/{post_id}')
async def update_post(post_id: int, update_post: CorrectPost, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = update(post).values(**update_post.dict()).where(post.c.id == post_id)
        await session.execute(stmt)
        await session.commit()

        return {
                "status": "success",
                "data": update_post,
                "details": "Пост обновлен"
            }
    except:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Неизвестная ошибка"
        })
