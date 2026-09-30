"""Shared fixtures for the API test suite."""

import time

import pytest
import requests

TIMEOUT = 30
RETRIES = 3
RETRY_BACKOFF = 1.0
RETRYABLE_STATUSES = {502, 503, 504}


class RetrySession(requests.Session):
    """Session that retries network errors and transient 5xx responses."""

    def request(self, method, url, **kwargs):
        last_exception = None
        for attempt in range(RETRIES):
            try:
                response = super().request(method, url, **kwargs)
                if response.status_code not in RETRYABLE_STATUSES:
                    return response
            except (requests.ConnectionError, requests.Timeout) as exc:
                last_exception = exc
            time.sleep(RETRY_BACKOFF * (attempt + 1))
        if last_exception is not None:
            raise last_exception
        return response


@pytest.fixture(scope="session")
def api_client():
    with RetrySession() as client:
        yield client
