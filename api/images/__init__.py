from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from gridfs.errors import NoFile
from motor.motor_asyncio import AsyncIOMotorGridFSBucket

from api.dependencies import get_fs
from api.images import crud
from api.types import ObjectId

router = APIRouter(tags=["images"])


@router.get("/{object_id}/", response_class=Response)
async def get_image(
    object_id: ObjectId, fs: AsyncIOMotorGridFSBucket = Depends(get_fs)
):
    try:
        grid_out = await crud.get_image(fs, object_id)
        return Response(await grid_out.read(), media_type=grid_out.content_type)
    except NoFile as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="image not found"
        ) from e
