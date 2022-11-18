from strawberry.types import Info

from api.graphql_app.schemas import Post
from api.posts.crud import get_posts


async def resolve_posts(info: Info, limit: int = 10, offset: int = 0) -> list[Post]:
    return [
        Post.from_db_model(post)
        async for post in get_posts(
            info.context.db, info.context.session, limit=limit, offset=offset
        )
    ]
