"""
Base fixtures for the test suites
"""
from decimal import Decimal
from typing import Callable, List, Optional

import pytest

from booking_sites_parser import Address, BaseSource, Parser, Property


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

    class NewSource(BaseSource):
        """
        New source class
        """
        id = 'new_source'
        domain = r'newsource\.com.*'

        title_css_selector = 'span.title'

        def get_description(self) -> str:
            """
            Get property description
            """

        def get_address(self) -> Address:
            """
            Get property description
            """

        def get_max_guests(self) -> int:
            """
            Get property maximum occupancy in guests
            """

        def get_price(self) -> Optional[Decimal]:
            """
            Get property price
            """

        def get_images(self) -> List[str]:
            """
            Get property list
            """

        def get_services(self) -> List[str]:
            """
            Get property services
            """

        def get_cancellation_policy(self) -> str:
            """
            Get property services
            """

    result = NewSource()
    result.url = 'https://newsource.com/?test=true'

    return result
