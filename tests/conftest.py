"""
Base fixtures for the test suites
"""
from typing import Callable

import pytest

from booking_sites_parser import Address, Airbnb, BaseSource, Parser, Property


@pytest.fixture
def patch_http_client(monkeypatch) -> Callable:
    """
    Patch HTTP client
    """
    client_path: str = 'booking_sites_parser.http_client.HttpClient.client.get'

    def _make_patch(response: Callable):
        monkeypatch.setattr(client_path, response)

    return _make_patch


@pytest.fixture
def base_parser() -> Parser:
    """
    Returns a base parser instance
    """
    return Parser()


@pytest.fixture
def base_property() -> Property:
    """
    Returns a base property instance
    """
    return Property('https://booking.com')


@pytest.fixture
def address() -> Address:
    """
    Returns a base address instance
    """
    return Address(address='street', region='region', country='country')


@pytest.fixture
def source() -> BaseSource:
    """
    Returns new source class
    """

    class NewSource(Airbnb):
        """
        New source class
        """
        id = 'new_source'
        domain = 'newsource.com'

    return NewSource()
