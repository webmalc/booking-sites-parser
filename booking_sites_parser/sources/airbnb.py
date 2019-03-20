"""
Airbnb module
"""

from decimal import Decimal
from typing import List, Optional

from booking_sites_parser.models import Address, BaseSource
from booking_sites_parser.sources.airbnb_mixin import AirbnbMixin


class Airbnb(BaseSource, AirbnbMixin):
    """
    Parser for airbnb.com website
    """

    id: str = 'airbnb'
    domain: str = r'airbnb((?!plus\/).)*'

    title_css_selector: str = 'span._18hrqvin'
    description_js_selector = ['sectioned_description', 'description']

    def get_description(self) -> str:
        """
        Get property description
        """
        return str(
            self.get_js_listing_node(*self.description_js_selector)) or ''

    def get_address(self) -> Address:
        """
        Get property description
        """

    def get_max_guests(self) -> int:
        """
        Get property maximum occupancy in guests
        """
        # ipdb> 'person_capacity' in  \
        # airbnb._js_data['reduxData']['homePDP']['listingInfo']['listing']

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
