"""
Airbnb module
"""
import json
from datetime import date, timedelta
from decimal import Decimal
from typing import Any, Callable, Iterable, List, Optional

from bs4 import BeautifulSoup

from booking_sites_parser.models import Address

from ..http_client import HttpClient, HttpResponse


class AirbnbMixin():
    """
    Mixin for Airbnb classes
    """

    parser: BeautifulSoup
    http_client: HttpClient
    _do_request: Callable[[object, str], HttpResponse]
    get_services: Callable[[object], List[Any]]

    _js_data: Optional[dict] = None
    _listing_price_data: Optional[dict] = None
    script_selector: str = 'script[data-state=true]'
    script_selector_fallback: str = 'script[data-hypernova-key=spaspabundlejs]'
    listing_path: List[str] = [
        'reduxData', 'homePDP', 'listingInfo', 'listing'
    ]
    price_url: str = (
        'https://www.airbnb.co.uk/api/v2/'
        'pdp_listing_booking_details?_format=for_web_with_date'
        '&_intents=p3_book_it&_interaction_type=dateChanged'
        '&check_in={check_in}&check_out={check_out}&currency=EUR'
        '&force_boost_unc_priority_message_type=&guests=1&key={key}'
        '&listing_id={id}&locale=en-GB&number_of_adults=1'
        '&number_of_children=0&number_of_infants=0')

    max_guests_js_selector: List[str] = ['person_capacity']
    amenities_js_selector: List[str] = ['listing_amenities']
    photos_js_selector: List[str] = ['photos']
    description_js_selector = ['sectioned_description', 'description']
    address_js_selectors: List[List[str]] = [
        ['p3_summary_address'],
        ['location_title'],
    ]
    api_key_js_path: List[str] = ['layout-init', 'api_config', 'key']

    def get_description(self) -> str:
        """
        Get property description
        """
        return str(
            self.get_js_listing_node(*self.description_js_selector)) or ''

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

    def get_js_listing_node(self, *args, root=False) -> Optional[Any]:
        """
        Get the listing information from the js data
        """
        result = None
        result = self.get_js_data()

        if not result:
            return None

        nodes = [] if root else self.listing_path[:]
        nodes += list(args)
        for node in nodes:
            if not isinstance(result, dict):
                return None
            result = result.get(node)
            if not result:
                return result
        return result

    def get_listing_price_data(self) -> Optional[dict]:
        """
        Get the property listing price data from the API
        """
        if self._listing_price_data:
            return self._listing_price_data

        property_id = self.get_id()
        api_key = self.get_api_key()
        date_format = '%Y-%m-%d'
        today = date.today()
        tommorow = today + timedelta(days=1)
        url = self.price_url.format(
            key=api_key,
            id=property_id,
            check_in=today.strftime(date_format),
            check_out=tommorow.strftime(date_format),
        )
        response = self._do_request(url)
        if not response.json:
            return None
        self._listing_price_data = response.json.get(
            'pdp_listing_booking_details')
        return self._listing_price_data

    def _get_services(self) -> List[Any]:
        """
        Get property amenities
        """
        return self.get_js_listing_node(*self.amenities_js_selector) or []

    def get_service_names(self) -> List[str]:
        """
        Get property amenities names
        """
        amenities = self.get_services()
        return [str(x.get('name')) for x in amenities]

    def get_price(self) -> Optional[Decimal]:
        """
        Get property price
        """
        listings = self.get_listing_price_data()
        if not listings or not isinstance(listings, list):
            return None
        data = listings.pop()
        rate = data.get('p3_display_rate')
        price = rate.get('amount') if rate else None
        if price:
            return Decimal(price)
        return None

    def get_id(self) -> Optional[int]:
        """
        Get the property ID
        """
        property_id = self.get_js_listing_node('id')
        if isinstance(property_id, str) and property_id.isnumeric():
            return int(property_id)
        return property_id

    def get_api_key(self) -> Optional[str]:
        """
        Get the API key
        """
        api_key = self.get_api_key_from_js_data()
        # if not api_key:
        #     api_key = self.get_api_key_from_html()
        return api_key

    def get_api_key_from_js_data(self) -> Optional[str]:
        """
        Get the API key from the JS data
        """
        return self.get_js_listing_node(*self.api_key_js_path, root=True)

    # def get_api_key_from_html(self) -> Optional[str]:
    #     """
    #     Get the API key from the HTML source
    #     """
    #     # self.parser.select_one('meta#_bootstrap-layout-init')['content']
    #     return 'incorrect api key'

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
