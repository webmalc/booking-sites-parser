"""
Airbnb module
"""

from decimal import Decimal
from typing import List, Optional

from booking_sites_parser.models import Address, BaseSource


class Airbnb(BaseSource):
    """
    Parser for airbnb.com website
    """

    id = 'airbnb'
    domain = 'airbnb'

    def get_title(self) -> str:
        """
        Get property title
        """

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
