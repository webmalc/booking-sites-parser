"""
Base fixtures for the test suites
"""
from decimal import Decimal
from typing import Callable, List, Optional

import pytest

from booking_sites_parser import Address, BaseSource, Parser, Property


@pytest.fixture
def airbnb_js_data() -> dict:
    """
    Returns a fake JS data for the Airbnb classes
    """
    return {
        'layout-init': {
            'api_config': {
                'key': 'api_key',
            }
        },
        'reduxData': {
            'homePDP': {
                'listingInfo': {
                    'listing': {
                        'id':
                        '777',
                        'photos': [
                            {
                                'sort_order': 2,
                                'large': 'image_2'
                            },
                            {
                                'xx_large': 'image_3'
                            },
                            {
                                'sort_order': 1,
                                'x_large': 'image_1'
                            },
                        ],
                        'person_capacity':
                        3,
                        'location_title':
                        'City, Region, Country',
                        'one': {
                            'two': {
                                'three': 'result'
                            }
                        },
                        'sectioned_description': {
                            'description': 'test_description'
                        }
                    }
                }
            }
        }
    }


@pytest.fixture
def patch_http_client(monkeypatch) -> Callable:
    """
    Patch HTTP client
    """
    client_path: str = 'booking_sites_parser.http_client.HttpClient.client.get'

    def _make_patch(response: Callable):
        monkeypatch.setattr(client_path, lambda x, headers: response(x))

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
        description_css_selector: str = 'div.description'

        def get_address(self) -> Optional[Address]:
            """
            Get property address
            """

        def get_max_guests(self) -> Optional[int]:
            """
            Get property maximum occupancy in guests
            """

        def get_price(self) -> Optional[Decimal]:
            """
            Get property price
            """

        def get_images(self) -> List[str]:
            """
            Get property images
            """

        def get_services(self) -> List[str]:
            """
            Get property services
            """

        def get_cancellation_policy(self) -> str:
            """
            Get property cancellation policy
            """

    result = NewSource()
    result.url = 'https://newsource.com/?test=true'

    return result
