"""
Airbnb module
"""
import json
from typing import Any, List, Optional

from bs4 import BeautifulSoup


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

    def get_max_guests(self) -> Optional[int]:
        """
        Get property maximum occupancy in guests
        """
        return self.get_js_listing_node(*self.max_guests_js_selector)

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
