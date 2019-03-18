"""
Airbnb module
"""

from decimal import Decimal
from typing import List, Optional

from booking_sites_parser.models import Address, BaseSource, ParserException


class Airbnb(BaseSource):
    """
    Parser for airbnb.com website
    """

    id: str = 'airbnb'
    domain: str = 'airbnb'
    title_selectors: List[str] = ['span._18hrqvin', 'span._1xzp5ma3']

    def get_title(self) -> str:
        """
        Get property title
        """
        for selector in self.title_selectors:
            element = self.parser.select_one(selector)
            if element:
                return element.text
        raise ParserException('Title element not found.')

    def get_description(self) -> str:
        """
        Get property description
        """

    def get_address(self) -> Address:
        """
        Get property description
        """

    def get_price(self) -> Optional[Decimal]:
        """
        Get property price
        """

    def get_images(self) -> List[str]:
        """
        Get property list
        """

    def get_services(self) -> List[str]:
        """
        Get property services
        """

    def get_cancellation_policy(self) -> str:
        """
        Get property services
        """
