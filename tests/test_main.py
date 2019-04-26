"""
Test suite for the main module
"""

from decimal import Decimal

from booking_sites_parser.__main__ import json_encode


def test_json_encode(base_property):
    """
    Json_encode should return a string with the JSON encoded property objects
    """
    base_property.title = 'Test property'
    base_property.description = 'Test property description'
    base_property.images = ['image one', 'image two']
    base_property.price = Decimal(12.33)
    base_property.services = [
        {
            'service_one': 'service_one'
        },
        {
            'service_two': 'service_two'
        },
    ]
    json_str = json_encode([base_property])

    assert json_str == '[{"url": "https://booking.com", \
"title": "Test property", "description": "Test property description", \
"images": ["image one", "image two"], \
"price": "12.3300000000000000710542735760100185871124267578125", \
"services": [{"service_one": "service_one"}, {"service_two": "service_two"}]}]'
