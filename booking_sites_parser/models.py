"""
Package models
"""
import re
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional

from .http_client import HttpClient


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
    source_id: str
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
    priority: int = 0
    url: Optional[str] = None
    url_regex_pattern: str = r'^https?:\/\/(www\.)?{domain}.*$'
    http_client: HttpClient = HttpClient()

    @property
    @abstractmethod
    def id(self) -> str:
        """
        Source ID
        """

    @property
    @abstractmethod
    def domain(self) -> str:
        """
        Domain to check if URL is suitable for this source
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

    def check_url(self, url: str = None) -> bool:
        """
        Check if the url is suitable for this source
        """
        if not url:
            url = self.url
        if not url:
            raise ParserException('URL has not been provided')

        pattern = re.compile(self.url_regex_pattern.format(domain=self.domain))
        return bool(pattern.match(url))

    def parse(self, url: str) -> Property:
        """
        Parse an URL and return a Property object
        :param url: an url to parse
        """
        self.url = url
        if not self.check_url(url):
            raise ParserException('Invalid URL has been provided')
        result = Property(url)
        result.source_id = self.id
        result.title = self.get_title()
        result.description = self.get_description()
        result.address = self.get_address()
        result.price = self.get_price()
        result.images = self.get_images()
        result.services = self.get_services()
        result.cancellation_policy = self.get_cancellation_policy()

        return result
