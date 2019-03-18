"""
Test suite for the airbnb source
"""

from typing import Callable

import pytest

from booking_sites_parser.http_client import HttpResponse
from booking_sites_parser.models import ParserException
from booking_sites_parser.sources.airbnb import Airbnb

PROPERTY_PLUS_URL: str = 'https://www.airbnb.co.uk/rooms/plus/4950937'
PROPERTY_PLUS_TITLE: str = 'Peaceful Treehouse with Ocean View'

PROPERTY_URL: str = 'https://www.airbnb.com/rooms/2075509'
PROPERTY_TITLE: str = 'Stunning home in central Tokyo'


def test_check_url():
    """
    Check_url should return true if the airbnb URLS provided
    """
    airbnb = Airbnb()
    assert airbnb.check_url(
        'https://www.airbnb.co.uk/rooms/111?guests=2&adults=1')

    assert airbnb.check_url('https://www.airbnb.com/rooms/12')
    assert airbnb.check_url('http://www.airbnb.com/rooms/12')
    assert airbnb.check_url('http://airbnb.ru/rooms/12')
    assert not airbnb.check_url('http://booking.com')


@pytest.mark.parametrize('url, expected, selector', [
    (PROPERTY_URL, PROPERTY_TITLE, '_18hrqvin'),
    (PROPERTY_PLUS_URL, PROPERTY_PLUS_TITLE, '_1xzp5ma3'),
])
def test_get_title(
        get_airbnb: Callable,
        url: str,
        expected: str,
        selector: str,
        patch_http_client,
):
    """
    Get_url should return a property title
    """
    html = '<span class="{}">{}</span>'.format(selector, expected)
    patch_http_client(lambda x: HttpResponse(200, html, True))
    airbnb = get_airbnb(url)
    title = airbnb.get_title()
    assert expected in title


@pytest.mark.http
@pytest.mark.parametrize('url, expected', [
    (PROPERTY_URL, PROPERTY_TITLE),
    (PROPERTY_PLUS_URL, PROPERTY_PLUS_TITLE),
])
def test_get_title_real_http(get_airbnb: Callable, url: str, expected: str):
    """
    Get_url should return a property title (real HTTP request)
    """
    airbnb = get_airbnb(url)
    title = airbnb.get_title()
    assert expected in title


def test_get_title_not_found():
    """
    Get_url should raise an exception if the title is not found
    """
    airbnb = Airbnb()
    airbnb.source_code = 'code without title'
    airbnb.get_parser()
    with pytest.raises(ParserException) as exception:
        airbnb.get_title()
    assert 'Title element not found.' in str(exception)
