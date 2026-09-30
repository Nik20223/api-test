"""Tests for the JSONPlaceholder API (https://jsonplaceholder.typicode.com/)."""

import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT = 30


def test_get_posts_returns_all_items(api_client):
    response = api_client.get(f"{BASE_URL}/posts", timeout=TIMEOUT)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 100
    assert {"userId", "id", "title", "body"} <= data[0].keys()


@pytest.mark.parametrize("post_id", [1, 5, 50])
def test_get_post_by_id(api_client, post_id):
    response = api_client.get(f"{BASE_URL}/posts/{post_id}", timeout=TIMEOUT)

    assert response.status_code == 200
    assert response.json()["id"] == post_id


@pytest.mark.parametrize("resource", ["users", "albums", "todos"])
def test_resource_endpoints_return_lists(api_client, resource):
    response = api_client.get(f"{BASE_URL}/{resource}", timeout=TIMEOUT)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data


def test_comments_filtered_by_post(api_client):
    response = api_client.get(
        f"{BASE_URL}/comments", params={"postId": 1}, timeout=TIMEOUT
    )

    assert response.status_code == 200
    data = response.json()
    assert data
    assert all(comment["postId"] == 1 for comment in data)


def test_create_post(api_client):
    payload = {"title": "foo", "body": "bar", "userId": 1}

    response = api_client.post(f"{BASE_URL}/posts", json=payload, timeout=TIMEOUT)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert "id" in data


def test_missing_post_returns_404(api_client):
    response = api_client.get(f"{BASE_URL}/posts/9999", timeout=TIMEOUT)

    assert response.status_code == 404
