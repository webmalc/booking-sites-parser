"""
Test suite for the booking source
"""
import pytest

from booking_sites_parser.models import Address
from booking_sites_parser.sources.booking import Booking

PROPERTY_URL: str = 'https://www.booking.com/hotel/gb/\
milestoneredcarnationhotels.en-gb.html'

PROPERTY_TITLE: str = 'Milestone Hotel Kensington'
PROPERTY_DESCRIPTION: str = 'Individually designed, each air-conditioned room \
offers a romantic elegance'

PROPERTY_ADDRESS: str = '1 Kensington Court, Kensington and Chelsea, \
London, W8 5DL, United Kingdom'

PROPERTY_IMAGE = 'images/hotel/max1024x768/260/26037489.jpg'


def test_check_url():
    """
    Check_url should return true if the booking URLS provided
    """
    bookign = Booking()

    assert bookign.check_url(
        'https://www.booking.com/hotel/ru/gostevoi-dom-svetlana-sochi123.html')

    assert bookign.check_url(
        'https://booking.com/hotel/gb/6-london-road.en-gb.html')

    assert bookign.check_url(
        'https://www.booking.com/hotel/de/holiday-inn-frankfurt-airport\
.en-gb.html?label=gen173nr-1DCAs')

    assert not bookign.check_url('http://airbnb.com')
    assert not bookign.check_url('http://bookign.ru')


@pytest.mark.http
def test_get_title_real_http():
    """
    Get_url should return the property title (real HTTP request)
    """
    booking = Booking()
    booking.url = PROPERTY_URL
    booking.get_parser()
    title = booking.get_title()
    assert PROPERTY_TITLE in title


@pytest.mark.http
def test_get_description_real_http():
    """
    Get_description should return the property description (real HTTP request)
    """
    booking = Booking()
    booking.url = PROPERTY_URL
    booking.get_parser()
    description = booking.get_description()
    assert PROPERTY_DESCRIPTION in description


@pytest.mark.http
def test_get_address_real_http():
    """
    Get_address should return the property address (real HTTP request)
    """
    booking = Booking()
    booking.url = PROPERTY_URL
    booking.get_parser()
    address = booking.get_address()
    assert isinstance(address, Address)
    assert PROPERTY_ADDRESS in str(address)


@pytest.mark.http
def test_get_images_real_http():
    """
    Get_address should return the property images (real HTTP request)
    """
    booking = Booking()
    booking.url = PROPERTY_URL
    booking.get_parser()
    images = booking.get_images()
    assert PROPERTY_IMAGE in images[0]


@pytest.mark.http
def test_get_services_real_http():
    """
    Get_price should return the list of property facilities (real HTTP request)
    """
    booking = Booking()
    booking.url = PROPERTY_URL
    booking.get_parser()
    facilities = booking.get_services()
    assert facilities[0].name == 'Tickets to attractions or shows'
    assert facilities[-1].name == 'Chinese'
    assert facilities[-1].category == 'Languages spoken'
    facilities_names = booking.get_service_names()
    assert 'Languages spoken: Turkish' in facilities_names
    assert 'Food & Drink: Breakfast in the room' in facilities_names
