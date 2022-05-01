from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from motor.motor_gridfs import AgnosticGridOut

from api.types import ObjectId


def get_image(fs: AsyncIOMotorGridFSBucket, object_id: ObjectId) -> AgnosticGridOut:
    return fs.open_download_stream(object_id)
