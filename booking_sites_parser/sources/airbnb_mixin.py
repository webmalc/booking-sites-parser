"""
Airbnb module
"""
import json
from typing import Any, Iterable, List, Optional

from bs4 import BeautifulSoup

from booking_sites_parser.models import Address


class AirbnbMixin():
    """
    Mixin for Airbnb classes
    """

    parser: BeautifulSoup
    _js_data: Optional[dict] = None
    script_selector: str = 'script[data-state=true]'
    script_selector_fallback: str = 'script[data-hypernova-key=spaspabundlejs]'
    listing_path: List[str] = [
        'reduxData', 'homePDP', 'listingInfo', 'listing'
    ]

    max_guests_js_selector: List[str] = ['person_capacity']
    photos_js_selector: List[str] = ['photos']
    address_js_selectors: List[List[str]] = [
        ['p3_summary_address'],
        ['location_title'],
    ]

    def get_address(self) -> Optional[Address]:
        """
        Get property address
        """
        result = None
        for path in self.address_js_selectors:
            address = self.get_js_listing_node(*path)
            result = Address.create_from_string(str(address))
        return result

    def get_max_guests(self) -> Optional[int]:
        """
        Get property maximum occupancy in guests
        """
        return self.get_js_listing_node(*self.max_guests_js_selector)

    def get_images(self) -> List[str]:
        """
        Get property images
        """
        photos = self.get_js_listing_node(*self.photos_js_selector)

        if not photos or not isinstance(photos, Iterable):
            return []
        photos = sorted(photos, key=lambda x: x.get('sort_order', 999))
        return [
            x.get('xx_large', x.get('x_large', x.get('large'))) for x in photos
        ]

    def get_js_listing_node(self, *args) -> Optional[Any]:
        """
        Get the listing information from the js data
        """
        result = None
        result = self.get_js_data()

        if not result:
            return None

        nodes = self.listing_path + list(args)
        for node in nodes:
            if not isinstance(result, dict):
                return None
            result = result.get(node)
            if not result:
                return result
        return result

    def get_js_data(self) -> Optional[dict]:
        """
        Get the main data from the inline js script
        """
        if self._js_data:
            return self._js_data

        fallback = False
        element = self.parser.select_one(self.script_selector)
        if not element:
            element = self.parser.select_one(self.script_selector_fallback)
        if element:
            try:
                self._js_data = json.loads(
                    element.text.replace('<!--', '').replace('-->', ''))
            except json.decoder.JSONDecodeError:
                return self._js_data
        if not fallback and element and isinstance(self._js_data, dict):
            self._js_data = self._js_data.get('bootstrapData')

        return self._js_data
