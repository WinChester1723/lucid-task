from pydantic import BaseModel, Field
from typing import List

class PostCreate(BaseModel):
    text: str = Field(..., max_length=1048576, description="The text of the post (up to 1 MB)")

class PostResponse(BaseModel):
    id: int = Field(..., description="Post ID")
    text: str = Field(..., description="The text of the post")

class PostListResponse(BaseModel):
    posts: List[PostResponse] = Field(..., description="List of user posts")