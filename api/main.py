from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import health, posts
from api.settings import Settings

settings = Settings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_headers=settings.ALLOW_METHODS,
)

app.include_router(posts.router)
app.include_router(health.router)
