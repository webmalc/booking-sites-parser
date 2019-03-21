"""
Package models
"""
import re
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional

from bs4 import BeautifulSoup

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
    parser: BeautifulSoup
    priority: int = 0
    url: Optional[str] = None
    url_regex_pattern: str = r'^https?:\/\/(www\.)?{domain}$'
    http_client: HttpClient = HttpClient()

    # CSS selectors
    title_css_selector: str
    description_css_selector: str

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
        Domain regex to check if URL is suitable for this source
        """

    def _get_html_text_by_selector(self, selector: str) -> str:
        """
        Get HTML element text by the selector
        """
        element = self.parser.select_one(selector)

        return getattr(element, 'text', '')

    def get_title(self) -> str:
        """
        Get property title
        """
        return self._get_html_text_by_selector(self.title_css_selector)

    def get_description(self) -> str:
        """
        Get property description
        """
        return self._get_html_text_by_selector(self.description_css_selector)

    @abstractmethod
    def get_max_guests(self) -> Optional[int]:
        """
        Get property maximum occupancy in guests
        """

    @abstractmethod
    def get_address(self) -> Address:
        """
        Get property address
        """

    @abstractmethod
    def get_price(self) -> Optional[Decimal]:
        """
        Get property price
        """

    @abstractmethod
    def get_images(self) -> List[str]:
        """
        Get property images
        """

    @abstractmethod
    def get_services(self) -> List[str]:
        """
        Get property services
        """

    @abstractmethod
    def get_cancellation_policy(self) -> str:
        """
        Get property cancellation policy
        """

    def __get_url(self, url: str = None) -> str:
        """
        Get URL
        """
        if not url:
            url = self.url
        if not url:
            raise ParserException('URL has not been provided.')
        return url

    def check_url(self, url: str = None) -> bool:
        """
        Check if the url is suitable for this source
        """
        url = self.__get_url(url)
        pattern = re.compile(self.url_regex_pattern.format(domain=self.domain))
        return bool(pattern.match(url))

    def get_source(self, url: str = None) -> str:
        """
        Get HTML source from URL
        :param url: source URL
        """
        self.source_code = ''
        url = self.__get_url(url)
        response = self.http_client.get(url)
        if not response.ok:
            raise ParserException('The HTTP request has failed.')
        self.source_code = response.text

        return self.source_code

    def get_parser(self) -> BeautifulSoup:
        """
        Get a parser for the source code
        """
        self.parser = None
        if not self.source_code:
            self.get_source()
        self.parser = BeautifulSoup(self.source_code, 'html.parser')

        return self.parser

    def parse(self, url: str) -> Property:
        """
        Parse an URL and return a Property object
        :param url: an url to parse
        """
        self.url = url
        if not self.check_url(url):
            raise ParserException('Invalid URL has been provided.')
        self.get_source(url)
        self.get_parser()
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
