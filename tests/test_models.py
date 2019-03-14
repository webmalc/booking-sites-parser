"""
Test suite for the parser models
"""
from booking_sites_parser import Address, Property


def test_property_id(base_property: Property):
    """
    Property should return an id equal to its URL
    """
    assert base_property.id == 'https://booking.com'


def test_propery_address(base_property: Property, address: Address):
    """
    Property address should be able to convert to string
    """
    base_property.address = address
    assert str(base_property.address) == 'street, region, country'

    base_property.address.address = None
    assert str(base_property.address) == 'region, country'

    base_property.address.region = None
    assert str(base_property.address) == 'country'
