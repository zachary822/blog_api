from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession

from api.types import ObjectId


def get_posts(
    client: AsyncIOMotorClient,
    session: AsyncIOMotorClientSession,
    *,
    q: Optional[str] = None,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
):
    pipeline = [
        {"$match": {"published": True}},
    ]

    if q:
        pipeline.insert(
            0,
            {
                "$search": {
                    "text": {"query": q, "path": ["title", "body"], "fuzzy": {}},  # type: ignore[dict-item]
                }
            },
        )
    else:
        pipeline.append({"$sort": {"created": -1}})  # type: ignore[dict-item]

    pipeline += [
        {"$skip": offset},  # type: ignore[dict-item]
        {"$limit": limit},  # type: ignore[dict-item]
    ]

    return client.blog.posts.aggregate(
        pipeline,
        session=session,
    )


def get_titles(client: AsyncIOMotorClient, session: AsyncIOMotorClientSession, q: str):
    return client.blog.posts.aggregate(
        [
            {"$search": {"autocomplete": {"query": q, "path": "title"}}},
            {"$match": {"published": True}},
            {"$limit": 20},
            {"$project": {"_id": 0, "title": 1}},
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
    {"$project": {"_id": 0, "year": "$_id.year", "month": "$_id.month", "count": 1}},
    {"$sort": {"year": -1, "month": -1}},
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
