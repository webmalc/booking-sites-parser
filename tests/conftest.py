# -*- coding: utf-8 -*-
"""
Base fixtures for the test suites
"""
import pytest

from booking_sites_parser import Address, Parser, Property


@pytest.fixture
def base_parser() -> Parser:
    """
    Returns a base parser instance
    """
    return Parser()


@pytest.fixture
def base_property() -> Property:
    """
    Returns a base property instance
    """
    return Property('https://booking.com')


@pytest.fixture
def address() -> Address:
    """
    Returns a base address instance
    """
    return Address('street', 'region', 'country')
