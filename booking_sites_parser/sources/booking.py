"""
Boooking.com module
"""

from decimal import Decimal
from typing import Any, List, Optional

from booking_sites_parser.models import BaseSource


class Booking(BaseSource):
    """
    Parser for airbnb.com website
    """

    id: str = 'booking'
    domain: str = r'booking.*'

    title_css_selector = 'h2#hp_hotel_name'
    description_css_selector = 'div#property_description_content'
    address_css_selector = 'p.address span.hp_address_subtitle'
    images_css_selector = 'div#photos_distinct a'

    def get_cancellation_policy(self) -> str:
        """
        Get property cancellation policy
        """

    def get_max_guests(self) -> Optional[int]:
        """
        Get property maximum occupancy in guests
        """

    def get_images(self) -> List[str]:
        """
        Get property images
        """
        images_links = self.parser.select(self.images_css_selector)
        return [
            i['href'].replace('max400', 'max1024x768') for i in images_links
        ]

    def _get_services(self) -> List[Any]:
        """
        Get property amenities
        """

    def get_service_names(self) -> List[str]:
        """
        Get property amenities names
        """

    def get_price(self) -> Optional[Decimal]:
        """
        Get property price
        """
