"""
Airbnb module
"""

from booking_sites_parser.models import BaseSource
from booking_sites_parser.sources.airbnb_mixin import AirbnbMixin


class Airbnb(AirbnbMixin, BaseSource):
    """
    Parser for airbnb.com website
    """

    id: str = 'airbnb'
    domain: str = r'airbnb((?!plus\/).)*'

    title_css_selector: str = 'span._18hrqvin'

    def get_cancellation_policy(self) -> str:
        """
        Get property cancellation policy
        """
