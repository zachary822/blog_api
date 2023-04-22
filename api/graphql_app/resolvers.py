from strawberry.types import Info

from api.graphql_app.schemas import Health, Post
from api.health import Status
from api.posts.crud import get_posts


async def resolve_posts(info: Info, limit: int = 10, offset: int = 0) -> list[Post]:
    return [
        Post.from_db_model(post)
        async for post in get_posts(
            info.context.db,
            info.context.session,
            limit=limit,
            offset=offset,
        )
    ]


async def resolve_health(info: Info):
    server_info = await info.context.client.server_info()
    return Health(status=Status.ok, mongo_version=server_info["version"])  # type: ignore[call-arg]
