#!/usr/bin/env python3
"""
Main file
"""

import requests
from functools import wraps
from typing import Callable
import redis


def count_request(method: Callable) -> Callable:
    """ track how many times a particular URL was accessed """
    client = redis.Redis()
    @wraps(method)
    def wrapper_function(url):
        """ wrap the decorated function and return the wrapper """
        client.incr(f"count:{url}")
        cached_content = client.get(f"cached:{url}")
        if cached_content:
            return cached_content.decode('utf-8')
        html = method(url)
        client.setex(f"cached:{url}", 10, html)
        return html
    return wrapper_function


@count_request
def get_page(url: str) -> str:
    """
    Parameters
    ----------
    url: str
        website url
    Returns
    -------
    str
        content of html page
    """
    request = requests.get(url)
    return request.text
