import yaml
from fastapi import FastAPI, Request, Response, status
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from gridfs.errors import NoFile

from api import health, images, posts
from api.settings import Settings

settings = Settings()

app = FastAPI(title="ThoughtBank Blog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_headers=settings.ALLOW_METHODS,
)

app.include_router(posts.router, prefix="/posts")
app.include_router(images.router, prefix="/images")
app.include_router(health.router, prefix="/health")


@app.exception_handler(NoFile)
def handle_gridfs_file_not_found(_request: Request, _exc: NoFile):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": "image not found"}
    )


@app.get("/openapi.yaml")
async def read_openapi_yaml() -> Response:
    openapi_json = app.openapi()
    return Response(
        await run_in_threadpool(
            yaml.dump, openapi_json, sort_keys=False, Dumper=yaml.Dumper
        ),
        media_type="text/yaml",
    )


@app.get("/")
def hello_world():
    return "Hello World!"
