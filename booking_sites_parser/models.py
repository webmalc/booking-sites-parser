"""
Package models
"""
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional


class ParserException(Exception):
    """
    Base parser exception
    """


class Address():
    """
    Address class
    """

    def __init__(
            self,
            country: str,
            address: str = None,
            region: str = None,
    ) -> None:
        """
        Class constructor

        :param address: address string
        """
        self.address = address
        self.region = region
        self.country = country

    def __str__(self) -> str:
        """
        Return a full address string
        """
        parts = [x for x in [self.address, self.region, self.country] if x]
        return ', '.join(parts)


class Property():
    """
    Property information
    """

    url: str
    title: str
    description: str
    address: Address
    price: Optional[Decimal]
    images: List[str] = []
    services: List[str] = []
    cancellation_policy: Optional[str]

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


class BaseSource(ABC):
    """
    Base class for sources classes (booking, airbnb, etc)
    """

    source_code: str = ''

    @property
    @abstractmethod
    def id(self):
        """
        Source ID
        """

    @abstractmethod
    def get_title(self) -> str:
        """
        Get property title
        """

    @abstractmethod
    def get_description(self) -> str:
        """
        Get property description
        """

    @abstractmethod
    def get_address(self) -> Address:
        """
        Get property description
        """

    @abstractmethod
    def get_price(self) -> Optional[Decimal]:
        """
        Get property price
        """

    @abstractmethod
    def get_images(self) -> List[str]:
        """
        Get property list
        """

    @abstractmethod
    def get_services(self) -> List[str]:
        """
        Get property services
        """

    @abstractmethod
    def get_cancellation_policy(self) -> str:
        """
        Get property services
        """
