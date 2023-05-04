import pendulum
from fastapi import APIRouter, Depends, status
from fastapi.responses import Response, StreamingResponse
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorGridFSBucket

from api.dependencies import get_fs, get_if_none_match, get_modified_since, get_session
from api.images import crud
from api.types import ObjectId

router = APIRouter(tags=["images"])


@router.get("/{object_id}/")
async def get_image(
    object_id: ObjectId,
    if_none_match: str | None = Depends(get_if_none_match),
    if_modified_since: pendulum.DateTime | None = Depends(get_modified_since),
    fs: AsyncIOMotorGridFSBucket = Depends(get_fs),
    session: AsyncIOMotorClientSession = Depends(get_session),
) -> Response:
    grid_out = await crud.get_image(fs, session, object_id)

    if if_none_match == grid_out.metadata["md5"] or (
        if_modified_since is not None and pendulum.instance(grid_out.upload_date) > if_modified_since
    ):
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)

    return StreamingResponse(
        crud.grid_iter(grid_out),
        media_type=grid_out.content_type,
        headers=crud.get_image_headers(grid_out),
    )
