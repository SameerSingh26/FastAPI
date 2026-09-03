from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, PostResponse

app = FastAPI()

text_posts={
    1: {"title": "New Post", "content": "cool text post"},
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


