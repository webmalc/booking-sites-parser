"""
HTTP client
"""
from abc import ABC, abstractmethod
from typing import Optional

import requests
from fake_useragent import UserAgent


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
    def text(self) -> str:
        """
        Status code
        """

    @property
    @abstractmethod
    def ok(self) -> bool:
        """
        Is the request successful
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
    text: str = ''
    json: Optional[dict] = None
    ok: bool = False

    def __init__(
            self,
            status_code: int = None,
            text: str = '',
            ok: bool = False,
            json: dict = None,
    ):
        """
        Class constructor
        :param status_code: int
        """
        self.status_code = status_code
        self.text = text
        self.json = json
        self.ok = ok


class HttpClient(BaseHttpClient):
    """
    Class for making HTTP requests
    """

    client = requests
    headers = {
        'user-agent': UserAgent().chrome,
        'cache-control': 'private, max-age=0, no-cache',
    }

    def get(self, url: str) -> HttpResponse:
        """
        Make GET request
        :param url: a requested URL
        """
        try:
            response = self.client.get(url, headers=self.headers)
        except requests.exceptions.RequestException:
            return HttpResponse()
        result = HttpResponse(response.status_code, response.text, response.ok)
        try:
            result.json = response.json()
        except (ValueError, TypeError):
            pass
        return result
