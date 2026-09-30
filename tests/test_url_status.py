"""Generic URL status test driven by the ``--url`` and ``--status_code`` options.

Usage:
    pytest tests/test_url_status.py --url=https://mail.ru --status_code=200
    pytest tests/test_url_status.py --url=https://ya.ru/sfhfh --status_code=404
"""

import pytest
import requests

TIMEOUT = 30


@pytest.fixture
def url(request):
    return request.config.getoption("--url")


@pytest.fixture
def status_code(request):
    return request.config.getoption("--status_code")


def test_url_returns_expected_status_code(url, status_code):
    response = requests.get(url, timeout=TIMEOUT)

    assert response.status_code == status_code, (
        f"Expected status {status_code} for {url}, got {response.status_code}"
    )
