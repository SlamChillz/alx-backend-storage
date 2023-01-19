#!/usr/bin/env python3
"""
Defines a function `get_page`
"""
import redis
import requests
rc = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """
    It uses the requests module to obtain
    the HTML content of a particular URL and returns it.
    Args:
        url (str): url whose content is to be fectched
    Returns:
        html (str): the HTML content of the url
    """
    rc.set(f"cached:{url}", count)
    resp = requests.get(url)
    rc.incr(f"count:{url}")
    rc.setex(f"cached:{url}", 10, rc.get(f"cached:{url}"))
    return resp.text
