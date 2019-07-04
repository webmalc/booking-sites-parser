"""
Test suite for the airbnb source
"""

from decimal import Decimal

import pytest

from booking_sites_parser.models import Address
from booking_sites_parser.sources.airbnb_plus import AirbnbPlus

PROPERTY_URL: str = 'https://www.airbnb.co.uk/rooms/plus/4950937'
PROPERTY_ID: int = 4950937
PROPERTY_TITLE: str = 'Peaceful Treehouse with Ocean View'
PROPERTY_DESCRIPTION: str = 'Enjoy panoramic ocean and forest views'
PROPERTY_ADDRESS: str = 'Aptos, California, United States'
PROPERTY_MAX_GUESTS: int = 6
PROPERTY_IMAGE = 'pictures/c10fc509-e309-4aad-b1af-7dd7c3ad880c.jpg'


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
def test_get_id_real_http():
    """
    Get_api_key should return the api key (real HTTP request)
    """
    airbnb = AirbnbPlus()
    airbnb.url = PROPERTY_URL
    airbnb.get_parser()
    assert airbnb.get_id() == PROPERTY_ID


@pytest.mark.http
def test_get_api_key_real_http():
    """
    Get_api_key should return the api key (real HTTP request)
    """
    airbnb = AirbnbPlus()
    airbnb.url = PROPERTY_URL
    airbnb.get_parser()
    api_key = airbnb.get_api_key()
    assert isinstance(api_key, str)
    assert len(api_key) >= 10


@pytest.mark.http
def test_get_title_real_http():
    """
    Get_title should return the property title (real HTTP request)
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
    the property max guests value (real HTTP request)
    """
    airbnb = AirbnbPlus()
    airbnb.url = PROPERTY_URL
    airbnb.get_parser()
    max_guests = airbnb.get_max_guests()
    assert max_guests == PROPERTY_MAX_GUESTS


@pytest.mark.http
def test_get_description_real_http():
    """
    Get_description should return the property description (real HTTP request)
    """
    airbnb = AirbnbPlus()
    airbnb.url = PROPERTY_URL
    airbnb.get_parser()
    description = airbnb.get_description()
    assert PROPERTY_DESCRIPTION in description


@pytest.mark.http
def test_get_address_real_http():
    """
    Get_address should return the property address (real HTTP request)
    """
    airbnb = AirbnbPlus()
    airbnb.url = PROPERTY_URL
    airbnb.get_parser()
    address = airbnb.get_address()
    assert isinstance(address, Address)
    assert PROPERTY_ADDRESS in str(address)


@pytest.mark.http
def test_get_images_real_http():
    """
    Get_description should return the list of
    property photos (real HTTP request)
    """
    airbnb = AirbnbPlus()
    airbnb.url = PROPERTY_URL
    airbnb.get_parser()
    photos = airbnb.get_images()
    assert PROPERTY_IMAGE in photos[0]


@pytest.mark.http
def test_get_price_real_http():
    """
    Get_price should return the property price (real HTTP request)
    """
    airbnb = AirbnbPlus()
    airbnb.url = PROPERTY_URL
    airbnb.get_parser()
    price = airbnb.get_price()
    assert isinstance(price, Decimal)
    assert 100 < price < 1000


@pytest.mark.http
def test_get_services_real_http():
    """
    Get_price should return the list of property amenities (real HTTP request)
    """
    airbnb = AirbnbPlus()
    airbnb.url = PROPERTY_URL
    airbnb.get_parser()
    amenities = [x.get('name') for x in airbnb.get_services()]
    assert 'TV' in amenities
    assert 'Air conditioning' in amenities
