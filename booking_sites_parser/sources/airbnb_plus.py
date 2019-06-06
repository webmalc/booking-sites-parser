"""
AirbnbPlus module
"""

from booking_sites_parser.models import BaseSource
from booking_sites_parser.sources.airbnb_mixin import AirbnbMixin


class AirbnbPlus(AirbnbMixin, BaseSource):
    """
    Parser for airbnb.com website (plus properties)
    """

    id: str = 'airbnb'
    domain: str = r'airbnb.*plus\/.*'

    def get_cancellation_policy(self) -> str:
        """
        Get property cancellation policy
        """
