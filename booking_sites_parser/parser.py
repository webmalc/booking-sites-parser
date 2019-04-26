"""
Parser module
"""
from typing import Iterable, Iterator, List, Tuple

from .models import BaseSource, Optional, ParserException, Property
from .sources.airbnb import Airbnb
from .sources.airbnb_plus import AirbnbPlus


class Parser():
    """
    Class for parsing the provided websites
    """

    _sources: List[BaseSource] = []

    def __init__(self, sources: List[BaseSource] = None):
        """
        Class constructor
        """
        if sources:
            self._sources = sources
        else:
            self._sources = [Airbnb(), AirbnbPlus()]

    def sort_sources_by_priority(self) -> None:
        """
        Sort the sources by their priority
        """
        self._sources.sort(key=lambda x: x.priority)

    def get_source(self, source_id: str) -> Tuple[int, BaseSource]:
        """
        Get a parser source by its ID

        :param id: a source ID
        :return tuple: a tuple with an id and  a source
        """
        for i, source in enumerate(self._sources):
            if source.id == source_id:
                return (i, source)
        raise ParserException(
            'Source with id={} has not been found.'.format(source_id))

    def set_source(self, source: BaseSource) -> None:
        """
        Add a source to the sources list or replace if it's already in the list

        :param source: a source to add
        """
        try:
            old_source_id = self.get_source(source.id)[0]
            self._sources[old_source_id] = source
        except ParserException:
            self._sources.append(source)

    @staticmethod
    def _try_source(source: BaseSource, url: str) -> Optional[Property]:
        """
        Try to get a property object from the source

        :param url: URL to parse
        :param source: source to try
        """
        result = None
        try:
            if source.check_url(url):
                result = source.parse(url)
        except ParserException:
            pass
        return result

    def parse(self, urls: Iterable[str]) -> Iterator[Property]:
        """
        Parse the provided urls list

        :param urls: an iterator object with urls to parse
        """
        for url in urls:
            for source in self._sources:
                result = self._try_source(source, url)
                if result:
                    yield result
