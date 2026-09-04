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

text_posts = {
    1:{"title":"New Post", "content":"This is a new post."},
    2: {"title": "Amazing Day", "content": "today is a great day"},
    3: {"title": "Learning Python", "content": "python is fun to learn"},
    4: {"title": "Data Engineering", "content": "data engineering is an exciting field"},
    5: {"title": "Good Morning", "content": "hope you have a wonderful morning"},
    6: {"title": "Keep Learning", "content": "never stop learning new things"},
    7: {"title": "Weekend Vibes", "content": "enjoying a relaxing weekend"},
    8: {"title": "Coding Time", "content": "time to write some awesome code"},
    9: {"title": "New Project", "content": "working on an interesting new project"},
    10: {"title": "Stay Positive", "content": "keep going and stay positive"}
    }

@app.get("/")
def read_root():
    return {"message": "FastAPI tutorial is running"}

@app.get("/posts") # @ is generally used in python for calling decorators. 
def get_all_posts(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")   
    return text_posts.get(id)

@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post


@app.post("/upload")
async def upload_file(
    file:UploadFile = File(...),
    caption: str = Form(...),
    session: AsyncSession = Depends(get_async_session)
):
    post = Post(
        caption = caption,
        url = "dummy_url",
        file_type = "photo",
        file_name = "dummy_name"
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": post.id,
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat()
            }
        )
    return {"posts": posts_data}

@app.delete("/posts/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session)):
    if post_id.isdigit():
        post_id_int = int(post_id)
        if post_id_int not in text_posts:
            raise HTTPException(status_code=404, detail="Post not found")
        del text_posts[post_id_int]
        return {"Success": True, "message": "Post deleted successfully"}

    try:
        post_uuid = uuid.UUID(post_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid post ID format")

    result = await session.execute(select(Post).where(Post.id == post_uuid))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await session.delete(post)
    await session.commit()
    return {"Success": True, "message": "Post deleted successfully"}