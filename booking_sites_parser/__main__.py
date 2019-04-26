"""The entry point for the booking-sites-parser"""
import argparse
import json
from typing import Iterator, List

from booking_sites_parser.models import Property
from booking_sites_parser.parser import Parser


def get_urls() -> List[str]:
    """
    Get URLs from the command line arguments
    """
    parser = argparse.ArgumentParser(description='Parse the provided URLs.')
    parser.add_argument('urls', type=str, nargs='+', help='urls to parse')
    args = parser.parse_args()
    return args.urls


def parse_urls(urls: List[str]) -> Iterator[Property]:
    """
    Parse the provided URLs.
    """
    parser = Parser()
    return parser.parse(urls)


def json_encode(results: Iterator[Property], indent=None) -> str:
    """
    Parse the results
    """
    return json.dumps(list(results),
                      indent=indent,
                      default=lambda x: getattr(x, '__dict__', str(x)))


def run():
    """
    Run the main code
    """
    print(json_encode(parse_urls(get_urls()), indent=4))


if __name__ == '__main__':
    run()
