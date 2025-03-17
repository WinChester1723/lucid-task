from fastapi import FastAPI
from src.routes.auth import router as auth_router
from src.routes.post import router as post_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(post_router)