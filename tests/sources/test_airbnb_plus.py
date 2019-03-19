"""
Test suite for the airbnb source
"""

import pytest

from booking_sites_parser.sources.airbnb_plus import AirbnbPlus

PROPERTY_URL: str = 'https://www.airbnb.co.uk/rooms/plus/4950937'
PROPERTY_TITLE: str = 'Peaceful Treehouse with Ocean View'


def test_check_url():
    """
    Check_url should return true if the airbnb URLS provided
    """
    airbnb = AirbnbPlus()

    assert airbnb.check_url(
        'https://www.airbnb.co.uk/rooms/plus/111?guests=2&adults=1')

    assert airbnb.check_url('https://www.airbnb.com/rooms/plus/12')
    assert airbnb.check_url('http://www.airbnb.com/rooms/plus/12')
    assert airbnb.check_url('http://airbnb.ru/rooms/plus/12')

    assert not airbnb.check_url('http://booking.com')
    assert not airbnb.check_url(
        'https://www.airbnb.co.uk/rooms/4950937?guests=1&adults=1')
    assert not airbnb.check_url('https://www.airbnb.com/rooms/12')


@pytest.mark.http
def test_get_title_real_http():
    """
    Get_url should return a property title (real HTTP request)
    """
    airbnb = AirbnbPlus()
    airbnb.url = PROPERTY_URL
    airbnb.get_parser()
    title = airbnb.get_title()
    assert PROPERTY_TITLE in title
