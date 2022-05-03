import pendulum
from fastapi import APIRouter, Depends
from fastapi.responses import Response, StreamingResponse
from motor.motor_asyncio import AsyncIOMotorGridFSBucket

from api.dependencies import get_fs
from api.images import crud
from api.types import ObjectId
from api.utils import to_rfc7231_format

router = APIRouter(tags=["images"])


@router.get("/{object_id}/", response_class=StreamingResponse)
async def get_image(
    object_id: ObjectId, fs: AsyncIOMotorGridFSBucket = Depends(get_fs)
):
    grid_out = await crud.get_image(fs, object_id)
    last_modified = pendulum.instance(grid_out.upload_date)
    return StreamingResponse(
        crud.grid_iter(grid_out),
        media_type=grid_out.content_type,
        headers={
            "Content-Length": str(grid_out.length),
            "Last-Modified": to_rfc7231_format(last_modified),
        },
    )


@router.head("/{object_id}/", response_class=Response)
async def get_image_headers(
    object_id: ObjectId, fs: AsyncIOMotorGridFSBucket = Depends(get_fs)
):
    grid_out = await crud.get_image(fs, object_id)
    last_modified = pendulum.instance(grid_out.upload_date)
    return Response(
        media_type=grid_out.content_type,
        headers={
            "Content-Length": str(grid_out.length),
            "Last-Modified": to_rfc7231_format(last_modified),
        },
    )
