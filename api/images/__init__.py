import pendulum
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from gridfs.errors import NoFile
from motor.motor_asyncio import AsyncIOMotorGridFSBucket

from api.dependencies import get_fs
from api.images import crud
from api.types import ObjectId

router = APIRouter(tags=["images"])


@router.api_route(
    "/{object_id}/", response_class=StreamingResponse, methods=["GET", "HEAD"]
)
async def get_image(
    object_id: ObjectId, fs: AsyncIOMotorGridFSBucket = Depends(get_fs)
):
    try:
        grid_out = await crud.get_image(fs, object_id)
        last_modified = pendulum.instance(grid_out.upload_date)
        return StreamingResponse(
            crud.grid_iter(grid_out),
            media_type=grid_out.content_type,
            headers={
                "Content-Length": str(grid_out.length),
                "Last-Modified": last_modified.format(
                    "ddd, DD MMM YYYY HH:mm:ss [GMT]"
                ),
            },
        )
    except NoFile as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="image not found"
        ) from e
