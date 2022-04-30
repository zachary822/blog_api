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

    def test_read_post_summary(self, client, mongodb_client):
        summary = [
            {
                "year": 2022,
                "month": 4,
                "count": 1,
            }
        ]

        mongodb_client.blog.posts.aggregate.return_value.__aiter__.return_value = (
            summary
        )

        response = client.get("/posts/summary/")
        assert response.status_code == 200
        assert response.json() == summary

    def test_read_month_posts(self, client, mongodb_client, post):
        posts = [post]

        mongodb_client.blog.posts.find.return_value.__aiter__.return_value = posts

        response = client.get("/posts/2022/4/")
        assert response.status_code == 200
        assert response.json() == posts
