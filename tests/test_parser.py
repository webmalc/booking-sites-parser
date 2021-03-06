"""
Test suite for the parser
"""

from collections.abc import Iterator
from typing import Callable

import pytest

from booking_sites_parser import BaseSource, Parser, ParserException, Property
from booking_sites_parser.http_client import HttpResponse
from booking_sites_parser.sources.airbnb import Airbnb
from booking_sites_parser.sources.airbnb_plus import AirbnbPlus
from booking_sites_parser.sources.booking import Booking
from tests.sources.test_airbnb import PROPERTY_TITLE as AIRBNB_TITLE
from tests.sources.test_airbnb import PROPERTY_URL as AIRBNB_URL
from tests.sources.test_airbnb_plus import PROPERTY_TITLE as AIRBNB_PLUS_TITLE
from tests.sources.test_airbnb_plus import PROPERTY_URL as AIRBNB_PLUS_URL


def test_parser_initialization(base_parser: Parser):
    """
    The parser should be able to be created
    """
    assert isinstance(base_parser, Parser)
    assert isinstance(base_parser._sources[0], Airbnb)  # pylint: disable=W0212
    assert isinstance(
        base_parser._sources[1],  # pylint: disable=W0212
        AirbnbPlus,
    )
    assert isinstance(
        base_parser._sources[2],  # pylint: disable=W0212
        Booking,
    )


def test_parser_initialization_with_sources(source):
    """
    The parser should be able to be created with injected sources
    """
    parser = Parser(sources=[source])
    assert parser._sources[0] == source  # pylint: disable=W0212


def test_parse_method_results_count(base_parser: Parser, source: BaseSource,
                                    patch_http_client: Callable):
    """
    Parse method should return an iterable object with a length
    equal to the number of valid URLs provided
    """
    html = '<title>Test HTML</title>'
    patch_http_client(lambda x: HttpResponse(200, html, True))
    base_parser._sources = [source]  # pylint: disable=W0212
    urls = [
        'https://www.newsource.com/one',
        'https://www.newsource.com/two',
        'invalid_url',
        'https://www.newsource.com/three',
    ]
    should_return_count = len(urls) - 1
    properties = base_parser.parse(urls)

    assert isinstance(properties, Iterator)
    result = next(properties)
    assert isinstance(result, Property)
    assert len(list(properties)) == should_return_count - 1


@pytest.mark.http
def test_parser_method_real_http(base_parser: Parser):
    """
    Parse method should return an iterable object with results
    """
    urls = [AIRBNB_URL, AIRBNB_PLUS_URL]
    results = base_parser.parse(urls)

    result = next(results)
    assert result.title == AIRBNB_TITLE
    result = next(results)
    assert result.title == AIRBNB_PLUS_TITLE
    with pytest.raises(StopIteration):
        next(results)


def test_sort_sources(base_parser: Parser, source: BaseSource):
    """
    Sort_sources_by_priority method should sort sources by their priority
    """
    source.priority = -1
    sources = base_parser._sources  # pylint: disable=W0212
    sources.append(source)
    assert sources[0].id == 'airbnb'
    base_parser.sort_sources_by_priority()
    assert sources[0].id == 'new_source'


def test_get_source(base_parser: Parser):
    """
    Get_source method should return a source by a source ID
    """
    source_id, airbnb = base_parser.get_source('airbnb')

    assert source_id == 0
    assert isinstance(airbnb, Airbnb)
    airbnb.id = 'test_val'
    assert base_parser._sources[0].id == 'test_val'  # pylint: disable=W0212


def test_get_source_with_invalid_id(base_parser: Parser):
    """
    Get_sourcee method should raise an exception
    when it's given an invalid source ID
    """
    with pytest.raises(ParserException) as exception:
        base_parser.get_source('invalid_source_id')

    assert 'id=invalid_source_id' in str(exception.value)


def test_set_source_add(base_parser: Parser, source: BaseSource):
    """
    Set_source should add a new source to the sources list
    """
    sources_list = base_parser._sources  # pylint: disable=W0212
    sources_len = len(sources_list)
    base_parser.set_source(source)

    assert len(sources_list) == sources_len + 1
    assert base_parser.get_source('new_source')[1].id == 'new_source'


def test_try_source_exception_suppression(base_parser: Parser,
                                          source: BaseSource):
    """
    Try_source method should suppress ParserException exceptions
    """

    def raise_exception(url: str):
        raise ParserException('test exception')

    source.check_url = raise_exception
    assert base_parser._try_source(  # pylint: disable=W0212
        source,
        'http://url.test',
    ) is None


def test_set_source_replace(base_parser: Parser):
    """
    Set_source method should replace a source if it's already in the list
    """
    sources_list = base_parser._sources  # pylint: disable=W0212
    sources_len = len(sources_list)
    airbnb_new = Airbnb()
    airbnb_new.source_code = 'new_airbnb'
    base_parser.set_source(airbnb_new)

    assert len(sources_list) == sources_len
    assert base_parser.get_source('airbnb')[1].source_code == 'new_airbnb'
