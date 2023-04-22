import orjson
import strawberry
from strawberry.fastapi import BaseContext, GraphQLRouter
from strawberry.http import GraphQLHTTPResponse

from api.dependencies import Client, Db, Session
from api.graphql_app.resolvers import resolve_health, resolve_posts
from api.graphql_app.schemas import Health, Post


@strawberry.type
class Query:
    posts: list[Post] = strawberry.field(resolve_posts)
    health: Health = strawberry.field(resolve_health)


schema = strawberry.Schema(Query)


class CustomContext(BaseContext):
    def __init__(self, client: Client, db: Db, session: Session):
        super().__init__()

        self.client = client
        self.db = db
        self.session = session


async def get_context(
    client: Client,
    db: Db,
    session: Session,
):
    return CustomContext(client, db, session)


class CustomGraphQLRouter(GraphQLRouter):
    def encode_json(self, data: GraphQLHTTPResponse) -> str:
        return orjson.dumps(data).decode()


router = GraphQLRouter(schema, context_getter=get_context)
