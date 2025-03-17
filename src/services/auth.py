from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.user import UserCreate, UserLogin
import hashlib
from jose import jwt
import secrets
from datetime import datetime, timedelta

SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_jwt_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(days=1)
    to_encode = {"sub": str(user_id), "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def signup(user: UserCreate, db: Session) -> str:
    if db.query(User).filter(User.email == user.email).first():
        raise ValueError("Email already exists")
    
    hashed_password = hash_password(user.password)
    
    db_user = User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    token = create_jwt_token(db_user.id)
    db_user.token = token
    db.commit()
    
    return token

def login(user: UserLogin, db: Session) -> str:
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or db_user.password != hash_password(user.password):
        raise ValueError("Invalid email or password")
    
    token = create_jwt_token(db_user.id)
    db_user.token = token
    db.commit()
    
    return token

def get_user_from_token(token: str, db: Session) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        user = db.query(User).filter(User.id == user_id, User.token == token).first()
        if not user:
            raise ValueError("Invalid token")
        return user
    except jwt.JWTError:
        raise ValueError("Invalid token")