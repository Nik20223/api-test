"""Tests for the Open Brewery DB API (https://www.openbrewerydb.org/)."""

import pytest

BASE_URL = "https://api.openbrewerydb.org/v1/breweries"
TIMEOUT = 30


def test_list_breweries_returns_full_objects(api_client):
    response = api_client.get(BASE_URL, params={"per_page": 10}, timeout=TIMEOUT)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data
    assert {"id", "name", "brewery_type"} <= data[0].keys()


@pytest.mark.parametrize("state", ["ohio", "california", "texas"])
def test_filter_breweries_by_state(api_client, state):
    response = api_client.get(
        BASE_URL, params={"by_state": state, "per_page": 10}, timeout=TIMEOUT
    )

    assert response.status_code == 200
    data = response.json()
    assert data
    assert all(brewery["state"].lower() == state for brewery in data)


@pytest.mark.parametrize("city", ["san_diego", "denver", "portland"])
def test_filter_breweries_by_city(api_client, city):
    response = api_client.get(
        BASE_URL, params={"by_city": city, "per_page": 10}, timeout=TIMEOUT
    )

    assert response.status_code == 200
    data = response.json()
    expected = city.replace("_", " ")
    assert data
    assert all(expected in brewery["city"].lower() for brewery in data)


def test_per_page_limits_result_size(api_client):
    response = api_client.get(BASE_URL, params={"per_page": 2}, timeout=TIMEOUT)

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_brewery_by_id(api_client):
    brewery_id = api_client.get(
        BASE_URL, params={"per_page": 1}, timeout=TIMEOUT
    ).json()[0]["id"]

    response = api_client.get(f"{BASE_URL}/{brewery_id}", timeout=TIMEOUT)

    assert response.status_code == 200
    assert response.json()["id"] == brewery_id


def test_search_returns_matching_breweries(api_client):
    response = api_client.get(
        f"{BASE_URL}/search",
        params={"query": "dog", "per_page": 10},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    data = response.json()
    assert data
    assert all("dog" in brewery["name"].lower() for brewery in data)


def test_unknown_brewery_returns_404(api_client):
    response = api_client.get(f"{BASE_URL}/not-a-real-id-123", timeout=TIMEOUT)

    assert response.status_code == 404
