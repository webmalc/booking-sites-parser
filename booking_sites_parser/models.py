# -*- coding: utf-8 -*-
"""
Package models
"""
from decimal import Decimal
from typing import List


class Address():
    """
    Address class
    """

    def __init__(self, address: str, region: str, country: str) -> None:
        """
        Class constructor

        :param address: address string
        """
        self.address = address
        self.region = region
        self.country = country

    def __str__(self):
        """
        Return a full address string
        """
        return '{}, {}, {}'.format(self.address, self.region, self.country)


class Property():
    """
    Property information
    """

    url: str
    title: str
    description: str
    address: Address
    price: Decimal
    images: List[str]
    services: List[str]
    cancellation_policy: str

    def __init__(self, url: str):
        """
        Class constructor

        :param url: property url
        """
        self.url = url

    @property
    def id(self) -> str:
        """ Get property ID """
        return self.url
