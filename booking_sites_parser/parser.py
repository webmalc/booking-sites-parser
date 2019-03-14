"""
Parser module
"""
from typing import Iterable, Iterator, List, Tuple

from .models import BaseSource, ParserException, Property
from .sources.airbnb import Airbnb


"""
Tuple with information about a property
"""


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
            self._sources = [Airbnb()]

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
            'source with id={} has not been found'.format(source_id))

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

    def parse(self, urls: Iterable[str]) -> Iterator[Property]:
        """
        Parse the provided urls list

        :param urls: an iterator object with urls to parse
        """
        for url in urls:
            result = Property(url)
            yield result
