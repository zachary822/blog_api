from typing import AsyncIterator

from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from motor.motor_gridfs import AgnosticGridOut

from api.types import ObjectId


def get_image(fs: AsyncIOMotorGridFSBucket, object_id: ObjectId) -> AgnosticGridOut:
    return fs.open_download_stream(object_id)


async def grid_iter(
    out: AgnosticGridOut, chunk_size: int = 4096
) -> AsyncIterator[bytes]:
    while True:
        content = await out.read(chunk_size)
        if not content:
            break
        yield content
