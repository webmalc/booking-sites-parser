# -*- coding: utf-8 -*-
"""
Parser module
"""
from typing import Iterable

from .models import Property


"""
Tuple with information about a property
"""


class Parser():
    """
    Class for parsing the provided websites
    """

    def parse(self, urls: Iterable[str]) -> Iterable[Property]:
        """
        Parse the provided urls list

        :param urls: a iterable object with urls to parse
        """
        for url in urls:
            result = Property(url)
            yield result
