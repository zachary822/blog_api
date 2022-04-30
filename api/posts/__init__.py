from typing import List

from fastapi import APIRouter, Depends, Path
from motor.motor_asyncio import AsyncIOMotorClient

from api.dependencies import CommonQueryParams, get_client
from api.posts import crud
from api.schemas import Month, ObjectId, Post

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[Post], response_model_by_alias=True)
async def read_posts(
    client: AsyncIOMotorClient = Depends(get_client),
    commons: CommonQueryParams = Depends(),
):
    posts = []

    async for post in crud.read_posts(client, **commons.dict()):
        posts.append(post)

    return posts


@router.get("/summary/", response_model=list[Month])
async def get_posts_summary(client: AsyncIOMotorClient = Depends(get_client)):
    posts = []

    async for post in crud.get_summary(client):
        posts.append(post)

    return posts


@router.get("/{object_id}/", response_model=Post, response_model_by_alias=True)
async def read_posts(
    object_id: ObjectId, client: AsyncIOMotorClient = Depends(get_client)
):
    return await crud.read_post(client, object_id)


@router.get("/{year}/{month}/", response_model=list[Post])
async def read_month_posts(
    year: int = Path(...),
    month: int = Path(..., le=12, ge=1),
    client: AsyncIOMotorClient = Depends(get_client),
):
    posts = []

    async for post in crud.get_month_posts(client, year, month):
        posts.append(post)

    return posts
