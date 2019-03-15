"""
Test suite for the parser models
"""
from decimal import Decimal
from unittest.mock import MagicMock

from booking_sites_parser import Address, BaseSource, Property


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


def test_sources_check_url_method(additional_source: BaseSource):
    """
    Check_url method should check if the url is suitable for the source
    """
    assert additional_source.check_url('https://newsource.com/?test=true&abc')
    assert additional_source.check_url('https://www.newsource.com')
    assert additional_source.check_url('http://www.newsource.com')
    assert not additional_source.check_url('https://google.com/')

    additional_source.domain = 'booking'
    assert additional_source.check_url('http://www.booking.com')
    assert additional_source.check_url('http://www.booking.ru')
    assert not additional_source.check_url('http://www.newsource.com')


def test_sources_parse_method(additional_source: BaseSource):
    """
    Parse method should call relevant methods of the source object
    and return a filled property object
    """
    title = 'test_title'
    description = 'test_description'
    address = Address('country', 'region', 'street')
    price = Decimal(12.3)
    images = ['image_one', 'image_two']
    services = ['service_one', 'service_two']
    cancellation_policy = 'policy'

    additional_source.get_title = MagicMock(return_value=title)
    additional_source.get_description = MagicMock(return_value=description)
    additional_source.get_address = MagicMock(return_value=address)
    additional_source.get_price = MagicMock(return_value=price)
    additional_source.get_images = MagicMock(return_value=images)
    additional_source.get_services = MagicMock(return_value=services)
    additional_source.get_cancellation_policy = MagicMock(
        return_value=cancellation_policy)

    result = additional_source.parse('https://newsource.com/?test=true')

    assert isinstance(result, Property)
    assert result.source_id == additional_source.id

    additional_source.get_title.assert_called_once()
    assert result.title == title

    additional_source.get_description.assert_called_once()
    assert result.description == description

    additional_source.get_address.assert_called_once()
    assert result.address == address

    additional_source.get_price.assert_called_once()
    assert result.price == price

    additional_source.get_images.assert_called_once()
    assert result.images == images

    additional_source.get_services.assert_called_once()
    assert result.services == services

    additional_source.get_cancellation_policy.assert_called_once()
    assert result.cancellation_policy == cancellation_policy
