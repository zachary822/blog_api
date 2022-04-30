import datetime

from fastapi import APIRouter, Depends, HTTPException, Path, status
from motor.motor_asyncio import AsyncIOMotorClient

from api.dependencies import CommonQueryParams, get_client
from api.posts import crud
from api.schemas import MonthSummary, Post
from api.types import ObjectId

router = APIRouter(tags=["posts"])


@router.get("/", response_model=list[Post], response_model_by_alias=True)
async def read_posts(
    client: AsyncIOMotorClient = Depends(get_client),
    commons: CommonQueryParams = Depends(),
):
    posts = []

    async for post in crud.get_posts(client, **commons.dict()):
        posts.append(post)

    return posts


@router.get("/summary/", response_model=list[MonthSummary])
async def read_posts_summary(client: AsyncIOMotorClient = Depends(get_client)):
    posts = []

    async for post in crud.get_summary(client):
        posts.append(post)

    return posts


@router.get("/{object_id}/", response_model=Post, response_model_by_alias=True)
async def read_posts(
    object_id: ObjectId, client: AsyncIOMotorClient = Depends(get_client)
):
    post = await crud.get_post(client, object_id)

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "post not found")

    return post


@router.get("/{year}/{month}/", response_model=list[Post], response_model_by_alias=True)
async def read_month_posts(
    year: int = Path(..., ge=datetime.MINYEAR, le=datetime.MAXYEAR),
    month: int = Path(..., le=12, ge=1),
    client: AsyncIOMotorClient = Depends(get_client),
):
    """
    Get posts for each month
    """
    posts = []

    async for post in crud.get_month_posts(client, year, month):
        posts.append(post)

    return posts
