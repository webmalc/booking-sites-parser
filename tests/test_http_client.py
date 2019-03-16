"""
Test suite for the HTTP client
"""
import pytest
import requests

from booking_sites_parser.http_client import (BaseHttpResponse, HttpClient,
                                              HttpResponse)


def _valid_request():
    """
    Make a valid request
    """

    client = HttpClient()
    response = client.get('https://example.com/')
    assert isinstance(response, BaseHttpResponse)
    assert response.status_code == 200
    assert '<title>Example Domain</title>' in response.text
    assert response.json is None


def _json_request():
    """
    Make an json request
    """

    client = HttpClient()
    response = client.get('https://api.github.com/')
    assert response.status_code == 200
    assert isinstance(response.json, dict)


def _invalid_request():
    """
    Make an invalid request
    """

    client = HttpClient()
    response = client.get('https://invalid.domain/')
    assert response.status_code is None
    assert response.text is None


def _invalid_request_404():
    """
    Make an invalid request 404
    """
    client = HttpClient()
    response = client.get('http://google.com/404')
    assert response.status_code == 404


def test_get(patch_http_client):
    """
    The client should be able to make GET request
    """

    def raise_exception():
        raise ValueError('json exception')

    response = HttpResponse(
        200,
        '<title>Example Domain</title>',
        raise_exception,
    )
    patch_http_client(lambda x: response)
    _valid_request()


def test_get_invalid(patch_http_client):
    """
    The client should be able to make GET request
    """

    def invalid_response(url: str):
        """
        Raises a requests exception
        """
        raise requests.exceptions.RequestException

    patch_http_client(invalid_response)
    _invalid_request()

    patch_http_client(lambda x: HttpResponse(404, '', lambda: None))
    _invalid_request_404()


def test_get_json(patch_http_client):
    """
    The client should be able to parse a JSON response (real HTTP request)
    """
    response = HttpResponse(200, '', lambda: {'test:': 'test_value'})
    patch_http_client(lambda x: response)
    _json_request()


@pytest.mark.http
def test_get_real_http():
    """
    The client should be able to make GET request (real HTTP request)
    """
    _valid_request()


@pytest.mark.http
def test_get_json_real_http():
    """
    The client should be able to parse a JSON response (real HTTP request)
    """
    _json_request()


@pytest.mark.http
def test_get_invalid_real_http():
    """
    The client should be able to process invalid URLs (real HTTP request)
    """
    _invalid_request()
    _invalid_request_404()
