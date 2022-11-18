import strawberry
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorDatabase
from strawberry.fastapi import BaseContext, GraphQLRouter

from api.dependencies import get_db, get_session
from api.graphql_app.resolvers import resolve_posts
from api.graphql_app.schemas import Post


@strawberry.type
class Query:
    posts: list[Post] = strawberry.field(resolve_posts)


schema = strawberry.Schema(Query)


class CustomContext(BaseContext):
    def __init__(self, db: AsyncIOMotorDatabase, session: AsyncIOMotorClientSession):
        super().__init__()

        self.db = db
        self.session = session


async def get_context(
    db: AsyncIOMotorDatabase = Depends(get_db),
    session: AsyncIOMotorClientSession = Depends(get_session),
):
    return CustomContext(db, session)


router = GraphQLRouter(schema, context_getter=get_context)
