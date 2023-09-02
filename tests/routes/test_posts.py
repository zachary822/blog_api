from unittest.mock import AsyncMock

import pytest


class TestPosts:
    @pytest.fixture
    def post(self):
        yield {
            "_id": "aaaaaaaaaaaaaaaaaaaaaaaa",
            "title": "blah",
            "created": "2022-04-30T00:00:00Z",
            "updated": "2022-04-30T00:00:00Z",
            "image": "http://example.com/test.png",
            "body": "blah",
            "tags": [],
            "summary": None,
        }

    def test_read_posts(self, client, mongodb_db, post):
        posts = [post]

        mongodb_db.posts.aggregate.return_value.__aiter__.return_value = posts

        response = client.get("/posts/")
        assert response.status_code == 200
        assert response.json() == posts

    def test_read_post_found(self, client, mongodb_db, post):
        mongodb_db.posts.find_one = AsyncMock(return_value=post)

        response = client.get("/posts/aaaaaaaaaaaaaaaaaaaaaaaa/")
        assert response.status_code == 200
        assert response.json() == post

    def test_read_post_not_found(self, client, mongodb_db, post):
        mongodb_db.posts.find_one = AsyncMock(return_value=None)

        response = client.get("/posts/aaaaaaaaaaaaaaaaaaaaaaaa/")
        assert response.status_code == 404

    def test_read_post_summary(self, client, mongodb_db):
        summary = {
            "monthly": [
                {
                    "year": 2022,
                    "month": 4,
                    "count": 1,
                },
            ],
            "tags": [{"name": "python", "count": 2}],
        }

        mongodb_db.posts.aggregate.return_value.__anext__.return_value = summary

        response = client.get("/posts/summary/")
        assert response.status_code == 200
        assert response.json() == summary

    def test_read_month_posts(self, client, mongodb_db, post):
        posts = [post]

        mongodb_db.posts.aggregate.return_value.__aiter__.return_value = posts

        response = client.get("/posts/2022/4/")
        assert response.status_code == 200
        assert response.json() == posts
