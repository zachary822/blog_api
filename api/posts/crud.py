from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from schemas import ObjectId
from bson.son import SON


def read_posts(
    client: AsyncIOMotorClient, limit: Optional[int] = 10, offset: Optional[int] = 0
):
    return (
        client.blog.posts.find({"published": True})
        .sort("created", -1)
        .limit(limit)
        .skip(offset)
    )


def read_post(client: AsyncIOMotorClient, object_id: ObjectId):
    return client.blog.posts.find_one({"_id": object_id, "published": True})


SUMMARY_PIPELINE = [
    {
        "$match": {
            "published": True,
        },
    },
    {
        "$group": {
            "_id": {
                "year": {"$year": "$created"},
                "month": {"$month": "$created"},
            },
            "count": {"$sum": 1},
        },
    },
    {"$sort": SON([("_id.year", -1), ("_id.month", -1)])},
]


def get_summary(client: AsyncIOMotorClient):
    return client.blog.posts.aggregate(SUMMARY_PIPELINE)


def get_month_posts(client: AsyncIOMotorClient, year: int, month: int):
    return client.blog.posts.find(
        {
            "$expr": {
                "$and": [
                    {"$eq": [{"$year": "$created"}, year]},
                    {"$eq": [{"$month": "$created"}, month]},
                    {"$eq": ["$published", True]},
                ],
            },
        }
    )
