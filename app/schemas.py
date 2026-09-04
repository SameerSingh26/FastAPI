from pydantic import BaseModel


class PostCreate(BaseModel):
    caption: str
    url: str
    file_type: str
    file_name: str

class PostResponse(BaseModel):
    title: str
    content: str