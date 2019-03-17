"""
Test suite for the parser models
"""
from decimal import Decimal
from unittest.mock import MagicMock

import pytest
import requests

from booking_sites_parser import Address, BaseSource, ParserException, Property
from booking_sites_parser.http_client import HttpResponse


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


def test_sources_check_url_method(source: BaseSource):
    """
    Check_url method should check if the url is suitable for the source
    """
    assert source.check_url('https://newsource.com/?test=true&abc')
    assert source.check_url('https://www.newsource.com')
    assert source.check_url('http://www.newsource.com')
    assert not source.check_url('https://google.com/')

    source.domain = 'booking'
    assert source.check_url('http://www.booking.com')
    assert source.check_url('http://www.booking.ru')
    assert not source.check_url('http://www.newsource.com')

    with pytest.raises(ParserException) as exception:
        assert source.check_url() is None
    assert 'URL has not been provided' in str(exception)


def test_sources_get_source_method(source: BaseSource, patch_http_client):
    """
    Get_source method should save HTML source to the source_code property
    and return a filled property object
    """
    html = '<title>Test HTML</title>'
    patch_http_client(lambda x: HttpResponse(200, html, True))
    source.url = 'http://newsource.com/12'
    source.get_source()
    assert source.source_code == html


def test_sources_get_source_method_exception(source: BaseSource,
                                             patch_http_client):
    """
    Get_source method should raise exception if a request has failed
    and return a filled property object
    """

    def invalid_response(url: str):
        """
        Raises a requests exception
        """
        raise requests.exceptions.RequestException

    source.source_code = 'old_source'
    patch_http_client(invalid_response)
    with pytest.raises(ParserException) as exception:
        source.get_source('http://newsource.com/12')
        assert source.source_code == ''
    assert 'The HTTP request has failed.' in str(exception)


def test_sources_parse_method(source: BaseSource, patch_http_client):
    """
    Parse method should call relevant methods of the source object
    and return a filled property object
    """
    html = '<title>Test HTML</title>'
    patch_http_client(lambda x: HttpResponse(200, html, True))
    title = 'test_title'
    description = 'test_description'
    address = Address('country', 'region', 'street')
    price = Decimal(12.3)
    images = ['image_one', 'image_two']
    services = ['service_one', 'service_two']
    cancellation_policy = 'policy'

    source.get_title = MagicMock(return_value=title)
    source.get_description = MagicMock(return_value=description)
    source.get_address = MagicMock(return_value=address)
    source.get_price = MagicMock(return_value=price)
    source.get_images = MagicMock(return_value=images)
    source.get_services = MagicMock(return_value=services)
    source.get_cancellation_policy = MagicMock(
        return_value=cancellation_policy)

    result = source.parse('https://newsource.com/?test=true')

    assert source.source_code == html
    assert isinstance(result, Property)
    assert result.source_id == source.id

    source.get_title.assert_called_once()
    assert result.title == title

    source.get_description.assert_called_once()
    assert result.description == description

    source.get_address.assert_called_once()
    assert result.address == address

    source.get_price.assert_called_once()
    assert result.price == price

    source.get_images.assert_called_once()
    assert result.images == images

    source.get_services.assert_called_once()
    assert result.services == services

    source.get_cancellation_policy.assert_called_once()
    assert result.cancellation_policy == cancellation_policy


def test_sources_parse_method_invalid_url(source: BaseSource):
    """
    Parse method should call raise an exception if the invalid URL is provided
    """

    with pytest.raises(ParserException) as exception:
        assert source.parse('https://invalid.url/') is None
    assert 'Invalid URL has been provided' in str(exception)
