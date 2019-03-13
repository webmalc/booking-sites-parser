# -*- coding: utf-8 -*-
"""
Test suite for the parser models
"""


def test_property_id(base_property):
    """
    Property should return an id equal to its URL
    """
    assert base_property.id == 'https://booking.com'


def test_propery_address(base_property, address):
    """
    Property address should be able to convert to string
    """
    base_property.address = address
    assert str(base_property.address) == 'street, region, country'
