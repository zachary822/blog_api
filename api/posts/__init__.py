import datetime
from dataclasses import asdict

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Response, status
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorDatabase
from pydantic import constr

from api.dependencies import CommonQueryParams, get_db, get_session
from api.posts import crud
from api.responses import RSSResponse
from api.schemas import MonthSummary, Post
from api.types import ObjectId
from api.utils import to_rfc7231_format

router = APIRouter(tags=["posts"])


@router.get("/", response_model=list[Post], response_model_by_alias=True)
async def read_posts(
    db: AsyncIOMotorDatabase = Depends(get_db),
    session: AsyncIOMotorClientSession = Depends(get_session),
    commons: CommonQueryParams = Depends(),
):
    posts = [post async for post in crud.get_posts(db, session, **asdict(commons))]

    if not posts and commons.q:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no posts returned by query"
        )

    return posts


@router.get("/summary/", response_model=list[MonthSummary])
async def read_posts_summary(
    db: AsyncIOMotorDatabase = Depends(get_db),
    session: AsyncIOMotorClientSession = Depends(get_session),
):
    return [post async for post in crud.get_summary(db, session)]


@router.get("/feed/", response_class=RSSResponse)
async def read_posts_feed(
    db: AsyncIOMotorDatabase = Depends(get_db),
    session: AsyncIOMotorClientSession = Depends(get_session),
):
    return RSSResponse(await crud.get_feed(db, session))


@router.post("/suggestions/")
async def suggest_title(
    body: constr(strip_whitespace=True, min_length=1) = Body(  # type: ignore[valid-type]
        ..., media_type="text/plain"
    ),
    db: AsyncIOMotorDatabase = Depends(get_db),
    session: AsyncIOMotorClientSession = Depends(get_session),
):
    return [t["title"] async for t in crud.get_titles(db, session, body)]


@router.get("/{object_id}/", response_model=Post, response_model_by_alias=True)
async def read_post(
    object_id: ObjectId,
    response: Response,
    db: AsyncIOMotorDatabase = Depends(get_db),
    session: AsyncIOMotorClientSession = Depends(get_session),
):
    post = await crud.get_post(db, session, object_id)

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "post not found")

    response.headers["Last-Modified"] = to_rfc7231_format(post["created"])

    return post


@router.get("/{year}/{month}/", response_model=list[Post], response_model_by_alias=True)
async def read_month_posts(
    year: int = Path(..., ge=datetime.MINYEAR, le=datetime.MAXYEAR),
    month: int = Path(..., le=12, ge=1),
    db: AsyncIOMotorDatabase = Depends(get_db),
    session: AsyncIOMotorClientSession = Depends(get_session),
):
    """
    Get posts for each month
    """
    return [post async for post in crud.get_month_posts(db, session, year, month)]
