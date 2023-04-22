from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from gridfs.errors import NoFile

import api.converters  # noqa
from api import graphql_app, health, images, posts
from api.dependencies import get_settings
from api.responses import YAMLResponse

settings = get_settings()

app = FastAPI(title="ThoughtBank Blog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_headers=settings.ALLOW_METHODS,
)

if settings.DEBUG:
    from api.middlewares import ProfilerMiddleware

    app.add_middleware(ProfilerMiddleware)

app.include_router(posts.router, prefix="/posts")
app.include_router(images.router, prefix="/images")
app.include_router(health.router, prefix="/health")
app.include_router(graphql_app.router, prefix="/graphql")


@app.exception_handler(NoFile)
def handle_gridfs_file_not_found(_request: Request, _exc: NoFile):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "image not found"})


@app.get(
    "/openapi.yaml",
    response_class=YAMLResponse,
)
async def read_openapi_yaml():
    return app.openapi()
