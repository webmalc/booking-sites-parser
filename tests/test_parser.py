# -*- coding: utf-8 -*-
"""
Test suite for the parser
"""

from collections.abc import Iterable

from booking_sites_parser import Parser, Property


def test_parser_initialization(base_parser):
    """
    The parser should be able to create
    """
    assert isinstance(base_parser, Parser)


def test_parser_method_results(base_parser):
    """
    Parse method should return an iterable object with results
    """
    properties = base_parser.parse(['one', 'two', 'three'])
    assert isinstance(properties, Iterable)
    assert isinstance(next(properties), Property)
