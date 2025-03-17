from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserLogin, UserResponse
from src.services.auth import signup, login
from src.models.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponse)
def signup_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    try:
        token = signup(user, db)
        return UserResponse(token=token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=UserResponse)
def login_endpoint(user: UserLogin, db: Session = Depends(get_db)):
    try:
        token = login(user, db)
        return UserResponse(token=token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))