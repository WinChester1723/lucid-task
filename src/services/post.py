from sqlalchemy.orm import Session
from src.models.post import Post
from src.models.user import User
from src.schemas.post import PostCreate, PostResponse
from cachetools import TTLCache
from typing import List

cache = TTLCache(maxsize=100, ttl=300)

def add_post(user: User, post: PostCreate, db: Session) -> int:
    db_post = Post(text=post.text, user_id=user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    cache.pop(user.id, None)
    
    return db_post.id

def get_posts(user: User, db: Session) -> List[PostResponse]:
    if user.id in cache:
        return cache[user.id]
    
    posts = db.query(Post).filter(Post.user_id == user.id).all()
    post_list = [PostResponse(id=post.id, text=post.text) for post in posts]
    
    cache[user.id] = post_list
    return post_list

def delete_post(user: User, post_id: int, db: Session) -> bool:
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == user.id).first()
    if not post:
        raise ValueError("Post not found or not authorized")
    
    db.delete(post)
    db.commit()
    
    cache.pop(user.id, None)
    
    return True