from unittest.mock import AsyncMock

import pytest


class TestPosts:
    @pytest.fixture
    def post(self):
        yield {
            "_id": "aaaaaaaaaaaaaaaaaaaaaaaa",
            "title": "blah",
            "created": "2022-04-30T00:00:00+00:00",
            "body": "blah",
        }

    def test_read_posts(self, client, mongodb_client, post):
        posts = [post]

        mongodb_client.blog.posts.aggregate.return_value.__aiter__.return_value = posts

        response = client.get("/posts/")
        assert response.status_code == 200
        assert response.json() == posts

    def test_read_post(self, client, mongodb_client, post):
        mongodb_client.blog.posts.find_one = AsyncMock(return_value=post)

        response = client.get("/posts/aaaaaaaaaaaaaaaaaaaaaaaa/")
        assert response.status_code == 200
        assert response.json() == post
