from fastapi import FastAPI
from src.routes.auth import router as auth_router
from src.routes.post import router as post_router
from src.models.database import Base, engine

app = FastAPI()

app.include_router(auth_router)
app.include_router(post_router)

Base.metadata.create_all(bind=engine)