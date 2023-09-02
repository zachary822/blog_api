import strawberry
from strawberry.fastapi import BaseContext, GraphQLRouter

from api.dependencies import Client, Db, Session
from api.graphql_app.resolvers import resolve_health, resolve_posts
from api.graphql_app.schemas import Health, Post


@strawberry.type
class Query:
    posts: list[Post] = strawberry.field(resolver=resolve_posts)
    health: Health = strawberry.field(resolver=resolve_health)  # type: ignore[assignment]


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


router: GraphQLRouter = GraphQLRouter(schema, context_getter=get_context)
