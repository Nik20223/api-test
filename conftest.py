"""Shared pytest configuration.

Registers the ``--url`` and ``--status_code`` command line options used by
the generic URL status test (see tests/test_url_status.py).
"""

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        default="https://ya.ru",
        help="URL to check the response status for (default: https://ya.ru)",
    )
    parser.addoption(
        "--status_code",
        default=200,
        type=int,
        help="Expected HTTP status code (default: 200)",
    )
