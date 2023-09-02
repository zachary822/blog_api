import datetime
from dataclasses import asdict

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Response, status
from pydantic import StringConstraints
from typing_extensions import Annotated

from api.dependencies import CommonQueryParams, Db, Session
from api.posts import crud
from api.posts.feed import RSS_SCHEMA
from api.responses import RSSResponse
from api.schemas import Post, Summary
from api.types import PydanticObjectId
from api.utils import to_rfc7231_format

router = APIRouter(tags=["posts"])


@router.get("/", response_model_by_alias=True)
async def read_posts(
    db: Db,
    session: Session,
    commons: CommonQueryParams = Depends(),
) -> list[Post]:
    posts = [post async for post in crud.get_posts(db, session, **asdict(commons))]

    if not posts and commons.q:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no posts returned by query")

    return posts


@router.get("/{object_id:oid}/", response_model_by_alias=True)
async def read_post(
    response: Response,
    db: Db,
    session: Session,
    object_id: PydanticObjectId,
) -> Post:
    post = await crud.get_post(db, session, object_id)

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "post not found")

    response.headers["Last-Modified"] = to_rfc7231_format(post["created"])

    return post


@router.get("/summary/")
async def read_posts_summary(
    db: Db,
    session: Session,
) -> Summary:
    return await anext(crud.get_summary(db, session))


@router.get(
    "/feed/",
    responses={status.HTTP_200_OK: {"content": {"application/rss+xml": {"schema": RSS_SCHEMA}}}},
)
async def read_posts_feed(
    db: Db,
    session: Session,
) -> RSSResponse:
    return RSSResponse(await crud.get_feed(db, session))


@router.post("/suggestions/")
async def suggest_title(
    db: Db,
    session: Session,
    body: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] = Body(..., media_type="text/plain"),  # type: ignore[valid-type] # noqa: E501
) -> list[str]:
    return [t["title"] async for t in crud.get_titles(db, session, body)]


@router.get("/tags/{tag}/")
async def read_tag_posts(
    tag: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)],  # type: ignore[valid-type]
    db: Db,
    session: Session,
) -> list[Post]:
    posts = [Post(**post) async for post in crud.get_tag_posts(db, session, tag)]

    if not posts:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "post not found")

    return posts


@router.get("/{year:int}/{month:int}/", response_model_by_alias=True)
async def read_month_posts(
    db: Db,
    session: Session,
    year: int = Path(..., ge=datetime.MINYEAR, le=datetime.MAXYEAR),
    month: int = Path(..., le=12, ge=1),
) -> list[Post]:
    """
    Get posts for each month
    """
    return [post async for post in crud.get_month_posts(db, session, year, month)]
