"""
HTTP client
"""
from abc import ABC, abstractmethod
from typing import Optional

import requests


class BaseHttpResponse(ABC):
    """
    Base class representing the HTTP response
    """

    @property
    @abstractmethod
    def status_code(self) -> Optional[int]:
        """
        Status code
        """

    @property
    @abstractmethod
    def text(self) -> Optional[str]:
        """
        Status code
        """

    @property
    @abstractmethod
    def json(self) -> Optional[dict]:
        """
        Status code
        """


class BaseHttpClient(ABC):
    """
    Base class for making HTTP requests
    """

    @abstractmethod
    def get(self, url: str) -> BaseHttpResponse:
        """
        Make GET request
        :param url: a requested URL
        """


class HttpResponse(BaseHttpResponse):
    """
    Class representing the HTTP response
    """
    status_code: Optional[int] = None
    text: Optional[str] = None
    json: Optional[dict] = None

    def __init__(
            self,
            status_code: int = None,
            text: str = None,
            json: dict = None,
    ):
        """
        Class constructor
        :param status_code: int
        """
        self.status_code = status_code
        self.text = text
        self.json = json


class HttpClient(BaseHttpClient):
    """
    Class for making HTTP requests
    """

    client = requests

    def get(self, url: str) -> HttpResponse:
        """
        Make GET request
        :param url: a requested URL
        """

        try:
            response = self.client.get(url)
        except requests.exceptions.RequestException:
            return HttpResponse()
        result = HttpResponse(response.status_code, response.text)
        try:
            result.json = response.json()
        except ValueError:
            pass
        return result
