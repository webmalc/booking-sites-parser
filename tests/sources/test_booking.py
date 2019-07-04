"""
Test suite for the booking source
"""
import pytest

from booking_sites_parser.http_client import HttpResponse
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


def test_get_images(patch_http_client):
    """
    Get_images should return the property images
    """
    html = '<div id="photos_distinct"><a href="/images/max400/1.jpg">\
</a><a href="/images/max400/2.png"></a></div>'

    patch_http_client(lambda x: HttpResponse(200, html, True))
    booking = Booking()
    booking.url = PROPERTY_URL
    booking.get_parser()
    images = booking.get_images()
    assert images == ['/images/max1024x768/1.jpg', '/images/max1024x768/2.png']


def test_get_services(patch_http_client):
    """
    Get_images should return the property facilities
    """
    html = '<div class="facilitiesChecklistSection"><h5>Category 1</h5>\
<ul><li>facility 1</li><li>facility 1.1</li></ul></div>'

    html += '<div class="facilitiesChecklistSection"><h5>Category 2</h5>\
<ul><li><span>facility 2</span></li></ul></div>'

    patch_http_client(lambda x: HttpResponse(200, html, True))
    booking = Booking()
    booking.url = PROPERTY_URL
    booking.get_parser()
    facilities = booking.get_services()

    assert facilities[0].category == 'Category 1'
    assert facilities[0].name == 'facility 1'
    assert facilities[1].category == 'Category 1'
    assert facilities[1].name == 'facility 1.1'
    assert facilities[2].category == 'Category 2'
    assert facilities[2].name == 'facility 2'

    facilities_names = booking.get_service_names()
    assert facilities_names == [
        'Category 1: facility 1', 'Category 1: facility 1.1',
        'Category 2: facility 2'
    ]


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
