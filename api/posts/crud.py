from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession

from api.types import ObjectId


def get_posts(
    client: AsyncIOMotorClient,
    session: AsyncIOMotorClientSession,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
):
    return client.blog.posts.aggregate(
        [
            {
                "$match": {
                    "published": True,
                },
            },
            {"$sort": {"created": -1}},
            {"$skip": offset},
            {"$limit": limit},
        ],
        session=session,
    )


def get_post(
    client: AsyncIOMotorClient, session: AsyncIOMotorClientSession, object_id: ObjectId
):
    return client.blog.posts.find_one(
        {"_id": object_id, "published": True}, session=session
    )


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
    {"$addFields": {"year": "$_id.year", "month": "$_id.month"}},
    {"$sort": {"_id.year": -1, "_id.month": -1}},
]


def get_summary(client: AsyncIOMotorClient, session: AsyncIOMotorClientSession):
    return client.blog.posts.aggregate(SUMMARY_PIPELINE, session=session)


def get_month_posts(
    client: AsyncIOMotorClient,
    session: AsyncIOMotorClientSession,
    year: int,
    month: int,
):
    return client.blog.posts.aggregate(
        [
            {
                "$match": {
                    "$expr": {
                        "$and": [
                            {"$eq": ({"$year": "$created"}, year)},
                            {"$eq": ({"$month": "$created"}, month)},
                            {"$eq": ("$published", True)},
                        ],
                    },
                }
            },
            {"$sort": {"created": -1}},
        ],
        session=session,
    )
