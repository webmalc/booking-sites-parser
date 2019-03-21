"""
Test suite for the airbnb mixin
"""
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
