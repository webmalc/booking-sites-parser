"""
Test suite for the airbnb source
"""

import pytest

from booking_sites_parser.sources.airbnb import Airbnb

PROPERTY_URL: str = 'https://www.airbnb.com/rooms/2075509'
PROPERTY_TITLE: str = 'Stunning home in central Tokyo'
PROPERTY_DESCRIPTION: str = 'We can also offer a concierge service to'
PROPERTY_MAX_GUESTS: int = 9
PROPERTY_IMAGE = '45604883/54451b1c_original.jpg?aki_policy=xx_large'


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


def test_get_title_description(airbnb_js_data):
    """
    Get_description should return a property description
    """
    airbnb = Airbnb()
    airbnb._js_data = airbnb_js_data  # pylint: disable=W0212
    assert airbnb.get_description() == 'test_description'


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
def test_get_max_guests_real_http():
    """
    Get_max_guests should return
    a property max guests value (real HTTP request)
    """
    airbnb = Airbnb()
    airbnb.url = PROPERTY_URL
    airbnb.get_parser()
    max_guests = airbnb.get_max_guests()
    assert max_guests == PROPERTY_MAX_GUESTS


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


@pytest.mark.http
def test_get_images_real_http():
    """
    Get_description should return a list of
    property photos (real HTTP request)
    """
    airbnb = Airbnb()
    airbnb.url = PROPERTY_URL
    airbnb.get_parser()
    photos = airbnb.get_images()
    assert PROPERTY_IMAGE in photos[0]
