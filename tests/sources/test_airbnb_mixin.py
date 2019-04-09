"""
Test suite for the airbnb mixin
"""
from decimal import Decimal

from booking_sites_parser.http_client import HttpResponse
from booking_sites_parser.sources.airbnb import Airbnb


def test_get_js_listing_node(airbnb_js_data):
    """
    Get_js_listing should return the js data node by a path
    """
    airbnb = Airbnb()
    airbnb._js_data = airbnb_js_data  # pylint: disable=W0212
    assert airbnb.get_js_listing_node('one', 'two', 'three') == 'result'
    assert airbnb.get_js_listing_node('one', 'two', 'invalid') is None
    assert airbnb.get_js_listing_node('one', 'two', 'three', 'four') is None
    assert airbnb.get_js_listing_node(
        'layout-init', 'api_config', 'key', root=True) == 'api_key'
    airbnb.get_js_data = lambda: None
    assert airbnb.get_js_listing_node('one') is None


def test_get_js_data_with_invalid_json():
    """
    Get_js_data should return None if the script contains an invalid JSON
    """
    airbnb = Airbnb()
    airbnb.source_code = """
    <html>
        <script data-state="true">invalid JSON markup</script>
    </html>
    """
    airbnb.get_parser()
    data = airbnb.get_js_data()
    assert data == airbnb._js_data  # pylint: disable=W0212
    assert data is None


def test_get_js_data_without_script():
    """
    Get_js_data should return None if the script tag is not found
    """
    airbnb = Airbnb()
    airbnb.source_code = """
    <html>
        <script data-state-invalid="true"></script>
    </html>
    """
    airbnb.get_parser()
    data = airbnb.get_js_data()
    assert data == airbnb._js_data  # pylint: disable=W0212
    assert data is None


def test_get_js_data():
    """
    Get_js_data should return the JS data from the source code (v1)
    """
    airbnb = Airbnb()
    airbnb.source_code = """
    <html>
        <script data-state="true">
            <!--{"bootstrapData": {"test": 12, "15": 11}}-->
        </script>
    </html>
    """
    airbnb.get_parser()
    data = airbnb.get_js_data()
    assert data == airbnb._js_data  # pylint: disable=W0212
    assert data == {'test': 12, '15': 11}


def test_get_js_data_fallback():
    """
    Get_js_data should return the JS data from the source code (fallback mode)
    """
    airbnb = Airbnb()
    airbnb.source_code = """
    <html>
        <script data-hypernova-key="spaspabundlejs">
            <!--{"bootstrapData": {"test": 12, "15": 11}}-->
        </script>
    </html>
    """
    airbnb.get_parser()
    data = airbnb.get_js_data()
    assert data == airbnb._js_data  # pylint: disable=W0212
    assert data == {'test': 12, '15': 11}


def test_get_max_guests(airbnb_js_data):
    """
    Get_max_guests should return a property max guests value
    """
    airbnb = Airbnb()
    airbnb._js_data = airbnb_js_data  # pylint: disable=W0212
    assert airbnb.get_max_guests() == 3


def test_get_images(airbnb_js_data):
    """
    Get_images should return a property images
    """
    airbnb = Airbnb()
    airbnb._js_data = airbnb_js_data  # pylint: disable=W0212
    assert airbnb.get_images() == ['image_1', 'image_2', 'image_3']


def test_get_address(airbnb_js_data):
    """
    Get_address should return a property address
    """
    airbnb = Airbnb()
    airbnb._js_data = airbnb_js_data  # pylint: disable=W0212
    assert str(airbnb.get_address()) == 'City, Region, Country'


def test_get_images_not_found():
    """
    Get_images should return an empty list if images are not found
    """
    airbnb = Airbnb()
    airbnb._js_data = {'test': 'test'}  # pylint: disable=W0212
    assert airbnb.get_images() == []


def test_get_api_key(airbnb_js_data):
    """
    Get_api_key should return the property api key
    """
    airbnb = Airbnb()
    airbnb._js_data = airbnb_js_data  # pylint: disable=W0212
    assert airbnb.get_api_key() == 'api_key'


def test_get_id(airbnb_js_data):
    """
    Get_api_key should return the property id
    """
    airbnb = Airbnb()
    airbnb._js_data = airbnb_js_data  # pylint: disable=W0212
    assert airbnb.get_id() == 777


def test_get_id_not_found():
    """
    Get_api_key should return None if the property ID is not found
    """
    airbnb = Airbnb()
    airbnb._js_data = {'test': 'test'}  # pylint: disable=W0212
    assert airbnb.get_id() is None


def test_get_price(patch_http_client, airbnb_js_data):
    """
    Get_price should return the property price
    """
    airbnb = Airbnb()
    price = '12.45'
    airbnb._js_data = airbnb_js_data  # pylint: disable=W0212
    details = {
        'pdp_listing_booking_details': [{
            'p3_display_rate': {
                'amount': price
            }
        }]
    }
    response = HttpResponse(200, '', True, lambda: details)
    patch_http_client(lambda x: response)
    price = airbnb.get_price()
    assert price == Decimal(price)


def test_get_price_not_found(patch_http_client, airbnb_js_data):
    """
    Get_price should return None if the property price is not found
    """
    airbnb = Airbnb()
    airbnb._js_data = airbnb_js_data  # pylint: disable=W0212
    response = HttpResponse(200, 'invalid response', True)
    patch_http_client(lambda x: response)
    price = airbnb.get_price()
    assert price is None

    airbnb._listing_price_data = 'invalid_listings'  # pylint: disable=W0212

    price = airbnb.get_price()
    assert price is None

    airbnb._listing_price_data = [  # pylint: disable=W0212
        {
            'p3_display_rate': {}
        }
    ]

    price = airbnb.get_price()
    assert price is None
