from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import health, posts
from api.settings import Settings

settings = Settings()

app = FastAPI(title="ThoughtBank Blog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_headers=settings.ALLOW_METHODS,
)

app.include_router(posts.router, prefix="/posts")
app.include_router(health.router, prefix="/health")


@app.get("/")
def hello_world():
    return "Hello World!"
