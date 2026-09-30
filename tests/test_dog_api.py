"""Tests for the Dog CEO API (https://dog.ceo/dog-api/)."""

import pytest

BASE_URL = "https://dog.ceo/api"
TIMEOUT = 30


def test_list_all_breeds(api_client):
    response = api_client.get(f"{BASE_URL}/breeds/list/all", timeout=TIMEOUT)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["message"], dict)
    assert "hound" in data["message"]


@pytest.mark.parametrize("breed", ["hound", "bulldog", "retriever"])
def test_breed_images_are_available(api_client, breed):
    response = api_client.get(f"{BASE_URL}/breed/{breed}/images", timeout=TIMEOUT)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"]
    assert all(image.startswith("https://") for image in data["message"])


@pytest.mark.parametrize("count", [1, 3, 5])
def test_random_images_count_matches_request(api_client, count):
    response = api_client.get(
        f"{BASE_URL}/breeds/image/random/{count}", timeout=TIMEOUT
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["message"]) == count


def test_random_image_returns_single_url(api_client):
    response = api_client.get(f"{BASE_URL}/breeds/image/random", timeout=TIMEOUT)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"].startswith("https://images.dog.ceo/")


def test_sub_breeds_list(api_client):
    response = api_client.get(f"{BASE_URL}/breed/hound/list", timeout=TIMEOUT)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "afghan" in data["message"]


def test_unknown_breed_returns_404(api_client):
    response = api_client.get(f"{BASE_URL}/breed/notabreed/images", timeout=TIMEOUT)

    assert response.status_code == 404
    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == 404
