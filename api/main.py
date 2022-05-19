from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from gridfs.errors import NoFile

from api import health, images, posts
from api.responses import YAMLResponse
from api.settings import Settings

settings = Settings()

app = FastAPI(title="ThoughtBank Blog API")


if settings.DEBUG:
    import pyinstrument

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        with pyinstrument.Profiler(async_mode="disabled") as p:
            response = await call_next(request)
        p.print()
        return response


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


@app.get(
    "/openapi.yaml",
    response_class=YAMLResponse,
)
async def read_openapi_yaml():
    return app.openapi()


@app.get("/")
def hello_world():
    return "Hello World!"
