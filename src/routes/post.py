from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.schemas.post import PostCreate, PostResponse, PostListResponse
from src.services.auth import get_user_from_token
from src.services.post import add_post, get_posts, delete_post
from src.models.database import get_db
from src.models.user import User

router = APIRouter(prefix="/posts", tags=["posts"])

def check_payload_size(request: Request):
    content_length = int(request.headers.get("content-length", 0))
    if content_length > 1048576:
        raise HTTPException(status_code=413, detail="Payload too large")

@router.post("/", response_model=PostResponse, dependencies=[Depends(check_payload_size)])
def add_post_endpoint(post: PostCreate, token: str, db: Session = Depends(get_db)):
    try:
        user = get_user_from_token(token, db)
        post_id = add_post(user, post, db)
        return PostResponse(id=post_id, text=post.text)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/", response_model=PostListResponse)
def get_posts_endpoint(token: str, db: Session = Depends(get_db)):
    try:
        user = get_user_from_token(token, db)
        posts = get_posts(user, db)
        return PostListResponse(posts=posts)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.delete("/{post_id}")
def delete_post_endpoint(post_id: int, token: str, db: Session = Depends(get_db)):
    try:
        user = get_user_from_token(token, db)
        delete_post(user, post_id, db)
        return {"message": "Post deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))