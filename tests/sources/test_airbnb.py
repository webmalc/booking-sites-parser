"""
Test suite for the airbnb source
"""
from booking_sites_parser.sources.airbnb import Airbnb


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
