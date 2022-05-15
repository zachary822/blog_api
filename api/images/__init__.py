from fastapi import APIRouter, Depends
from fastapi.responses import Response, StreamingResponse
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorGridFSBucket

from api.dependencies import get_fs, get_session
from api.images import crud
from api.types import ObjectId

router = APIRouter(tags=["images"])


@router.get("/{object_id}/", response_class=StreamingResponse)
async def get_image(
    object_id: ObjectId,
    fs: AsyncIOMotorGridFSBucket = Depends(get_fs),
    session: AsyncIOMotorClientSession = Depends(get_session),
):
    grid_out = await crud.get_image(fs, session, object_id)
    return StreamingResponse(
        crud.grid_iter(grid_out),
        media_type=grid_out.content_type,
        headers=crud.get_image_headers(grid_out),
    )


@router.head("/{object_id}/", response_class=Response)
async def get_image_headers(
    object_id: ObjectId,
    fs: AsyncIOMotorGridFSBucket = Depends(get_fs),
    session: AsyncIOMotorClientSession = Depends(get_session),
):
    grid_out = await crud.get_image(fs, session, object_id)
    return Response(
        media_type=grid_out.content_type,
        headers=crud.get_image_headers(grid_out),
    )
