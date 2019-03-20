"""
AirbnbPlus module
"""

from decimal import Decimal
from typing import List, Optional

from booking_sites_parser.models import Address, BaseSource
from booking_sites_parser.sources.airbnb_mixin import AirbnbMixin


class AirbnbPlus(BaseSource, AirbnbMixin):
    """
    Parser for airbnb.com website (plus properties)
    """

    id: str = 'airbnb'
    domain: str = r'airbnb.*plus\/.*'

    title_css_selector: str = 'span._1xzp5ma3'
    description_css_selector: str = 'div._9qwh472 span._1ezjrwzo'

    def get_address(self) -> Address:
        """
        Get property description
        """

    def get_max_guests(self) -> int:
        """
        Get property maximum occupancy in guests
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
