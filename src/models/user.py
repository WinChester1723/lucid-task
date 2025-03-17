from sqlalchemy import Column, Integer, String
from src.models.database import Base
from src.models.post import Post
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    token = Column(String(512), nullable=True)
    posts = relationship("Post", back_populates="user")