import uuid

from fastapi import FastAPI, HTTPException, File , UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse
from app.databaseconnect import Post, create_database_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select



@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_database_and_tables()
    yield 


app = FastAPI(lifespan=lifespan)

@app.get("/posts" )
async def get_post(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post))
    return result.scalars().all()

@app.get("/posts/{post_id}" )
async def get_post(session: AsyncSession = Depends(get_async_session), post_id: uuid.UUID = None):
    result = await session.execute(select(Post).filter(Post.id == post_id))
    return result.scalars().all()

@app.post("/posts")
async def create_post(
    post: PostCreate,
    session: AsyncSession = Depends(get_async_session)
):
    new_post = Post(
        caption=post.caption,
        url=post.url,
        file_type=post.file_type,
        file_name=post.file_name
    )
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return new_post

@app.delete("/posts/{post_id}")
async def delete_post(
    post_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).filter(Post.id == post_id))
    post_to_delete = result.scalars().first()
    if not post_to_delete:
        raise HTTPException(status_code=404, detail="Post not found")
    await session.delete(post_to_delete)
    await session.commit()
    return {"message": "Post deleted successfully"}

    





