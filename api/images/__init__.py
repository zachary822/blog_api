from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from gridfs.errors import NoFile
from motor.motor_asyncio import AsyncIOMotorGridFSBucket

from api.dependencies import get_fs
from api.types import ObjectId

router = APIRouter(tags=["images"])


@router.get("/{object_id}/", response_class=StreamingResponse)
async def get_image(
    object_id: ObjectId, fs: AsyncIOMotorGridFSBucket = Depends(get_fs)
):
    try:
        grid_out = await fs.open_download_stream(object_id)

        async def read():
            while True:
                content = await grid_out.read(1024)
                if not content:
                    break
                yield content

    except NoFile as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="image not found"
        ) from e

    return StreamingResponse(
        read(),
        media_type=grid_out.content_type,
        headers={"Content-Length": str(grid_out.length)},
    )
