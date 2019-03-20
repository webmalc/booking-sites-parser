"""
Test suite for the airbnb source
"""

import pytest

from booking_sites_parser.sources.airbnb import Airbnb

PROPERTY_URL: str = 'https://www.airbnb.com/rooms/2075509'
PROPERTY_TITLE: str = 'Stunning home in central Tokyo'
PROPERTY_DESCRIPTION: str = 'We can also offer a concierge service to'


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
    assert not airbnb.check_url(
        'https://www.airbnb.co.uk/rooms/plus/4950937?guests=1&adults=1')


@pytest.mark.http
def test_get_title_real_http():
    """
    Get_url should return a property title (real HTTP request)
    """
    airbnb = Airbnb()
    airbnb.url = PROPERTY_URL
    airbnb.get_parser()
    title = airbnb.get_title()
    assert PROPERTY_TITLE in title


@pytest.mark.http
def test_get_description_real_http():
    """
    Get_description should return a property description (real HTTP request)
    """
    airbnb = Airbnb()
    airbnb.url = PROPERTY_URL
    airbnb.get_parser()
    description = airbnb.get_description()
    assert PROPERTY_DESCRIPTION in description
