from http import HTTPStatus

import pytest


POST_SCHEMA = {
    "userId": int,
    "id": int,
    "title": str,
    "body": str,
}


def assert_post_schema(post: dict) -> None:
    assert isinstance(post, dict), "Response body should be a JSON object"

    for field_name, field_type in POST_SCHEMA.items():
        assert field_name in post, f"Missing field: {field_name}"
        assert isinstance(post[field_name], field_type), (
            f"Field '{field_name}' should be {field_type.__name__}"
        )


@pytest.mark.smoke
def test_get_single_post_returns_expected_schema(api_client) -> None:
    response = api_client.get("/posts/1")

    assert response.status_code == HTTPStatus.OK

    post = response.json()
    assert_post_schema(post)
    assert post["id"] == 1


@pytest.mark.smoke
def test_get_posts_list_is_not_empty(api_client) -> None:
    response = api_client.get("/posts")

    assert response.status_code == HTTPStatus.OK

    posts = response.json()
    assert isinstance(posts, list), "Posts endpoint should return a list"
    assert posts, "Posts list should not be empty"
    assert_post_schema(posts[0])


@pytest.mark.regression
def test_create_post_returns_created_entity(api_client) -> None:
    payload = {
        "title": "qa portfolio post",
        "body": "Created by pytest API test example",
        "userId": 10,
    }

    response = api_client.post("/posts", json=payload)

    assert response.status_code == HTTPStatus.CREATED

    created_post = response.json()
    assert created_post["title"] == payload["title"]
    assert created_post["body"] == payload["body"]
    assert created_post["userId"] == payload["userId"]
    assert "id" in created_post


@pytest.mark.negative
def test_unknown_endpoint_returns_404(api_client) -> None:
    response = api_client.get("/unknown-endpoint")

    assert response.status_code == HTTPStatus.NOT_FOUND
