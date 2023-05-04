import pendulum
from fastapi import APIRouter, Depends, status
from fastapi.responses import Response, StreamingResponse
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorGridFSBucket

from api.dependencies import CacheControl, get_fs, get_session
from api.images import crud
from api.types import ObjectId

router = APIRouter(tags=["images"])

cache_control = CacheControl()


@router.get("/{object_id}/")
async def get_image(
    object_id: ObjectId,
    is_not_modified=Depends(cache_control),
    fs: AsyncIOMotorGridFSBucket = Depends(get_fs),
    session: AsyncIOMotorClientSession = Depends(get_session),
) -> Response:
    grid_out = await crud.get_image(fs, session, object_id)

    if is_not_modified(grid_out.metadata["md5"], pendulum.instance(grid_out.upload_date)):
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)

    return StreamingResponse(
        crud.grid_iter(grid_out),
        media_type=grid_out.content_type,
        headers=crud.get_image_headers(grid_out),
    )
