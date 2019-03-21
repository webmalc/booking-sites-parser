"""
Test suite for the airbnb source
"""

import pytest

from booking_sites_parser.sources.airbnb_plus import AirbnbPlus

PROPERTY_URL: str = 'https://www.airbnb.co.uk/rooms/plus/4950937'
PROPERTY_TITLE: str = 'Peaceful Treehouse with Ocean View'
PROPERTY_DESCRIPTION: str = 'Rest well, then wake up to explore'
PROPERTY_MAX_GUESTS: int = 6


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
    Get_title should return a property title (real HTTP request)
    """
    airbnb = AirbnbPlus()
    airbnb.url = PROPERTY_URL
    airbnb.get_parser()
    title = airbnb.get_title()
    assert PROPERTY_TITLE in title


@pytest.mark.http
def test_get_max_guests_real_http():
    """
    Get_max_guests should return
    a property max guests value (real HTTP request)
    """
    airbnb = AirbnbPlus()
    airbnb.url = PROPERTY_URL
    airbnb.get_parser()
    max_guests = airbnb.get_max_guests()
    assert max_guests == PROPERTY_MAX_GUESTS


@pytest.mark.http
def test_get_description_real_http():
    """
    Get_description should return a property description (real HTTP request)
    """
    airbnb = AirbnbPlus()
    airbnb.url = PROPERTY_URL
    airbnb.get_parser()
    description = airbnb.get_description()
    assert PROPERTY_DESCRIPTION in description
