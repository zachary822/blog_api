from typing import Any, Optional

from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorDatabase

from api.posts.feed import Feed
from api.schemas import Post
from api.types import PydanticObjectId


def get_posts(
    db: AsyncIOMotorDatabase,
    session: AsyncIOMotorClientSession,
    *,
    q: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
):
    pipeline: list[dict[str, Any]] = [
        {"$match": {"published": True}},
        {"$project": {"published": 0}},
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
        pipeline.append({"$sort": {"created": -1, "_id": -1}})  # type: ignore[dict-item]

    if offset > 0:
        pipeline.append({"$skip": offset})

    pipeline.append({"$limit": limit})

    return db.posts.aggregate(
        pipeline,
        session=session,
    )


def get_titles(db: AsyncIOMotorDatabase, session: AsyncIOMotorClientSession, q: str):
    return db.posts.aggregate(
        [
            {"$search": {"autocomplete": {"query": q, "path": "title", "fuzzy": {}}}},
            {"$match": {"published": True}},
            {"$limit": 20},
            {"$project": {"_id": 0, "title": 1}},
        ],
        session=session,
    )


def get_post(db: AsyncIOMotorDatabase, session: AsyncIOMotorClientSession, object_id: PydanticObjectId):
    return db.posts.find_one({"_id": object_id, "published": True}, session=session)


SUMMARY_PIPELINE = [
    {
        "$facet": {
            "monthly": [
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
                {
                    "$project": {
                        "_id": 0,
                        "year": "$_id.year",
                        "month": "$_id.month",
                        "count": 1,
                    }
                },
                {"$sort": {"year": -1, "month": -1}},
            ],
            "tags": [
                {"$match": {"published": True}},
                {"$unwind": {"path": "$tags"}},
                {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
                {"$project": {"_id": 0, "name": "$_id", "count": 1}},
                {"$sort": {"count": -1, "name": -1}},
            ],
        }
    }
]


def get_summary(db: AsyncIOMotorDatabase, session: AsyncIOMotorClientSession):
    return db.posts.aggregate(SUMMARY_PIPELINE, session=session)


def get_month_posts(
    db: AsyncIOMotorDatabase,
    session: AsyncIOMotorClientSession,
    year: int,
    month: int,
):
    return db.posts.aggregate(
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


def get_tag_posts(
    db: AsyncIOMotorDatabase,
    session: AsyncIOMotorClientSession,
    tag: str,
):
    return db.posts.aggregate(
        [
            {
                "$match": {
                    "$expr": {
                        "$and": [
                            {"$in": (tag, "$tags")},
                            {"$eq": ("$published", True)},
                        ],
                    },
                }
            },
            {"$sort": {"created": -1}},
        ],
        session=session,
    )


async def get_feed(
    db: AsyncIOMotorDatabase,
    session: AsyncIOMotorClientSession,
):
    return Feed(
        title="ThoughtBank Blog",
        link="https://blog.thoughtbank.app/",
        feed_link="https://api.thoughtbank.app/posts/feed/",
        posts=[Post(**post) async for post in get_posts(db, session)],
        description="All manners of tech posts.",
    ).to_etree()
