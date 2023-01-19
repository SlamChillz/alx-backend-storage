#!/usr/bin/env python3
"""
Defines a Cache class that implements redis storage implicitly
"""
import uuid
import redis
from functools import wraps
from typing import Union, Callable


def call_history(method: Callable) -> Callable:
    """
    Create and return function that stores
    the inputs and outputs each time a method is called
    Args:
        method (Calllable): function to be wrapped
    Returns:
        A wrapper function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Stores input and output values of a method
        """
        input_key = method.__qualname__ + ':inputs'
        output_key = method.__qualname__ + ':outputs'
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, output)
        return output
    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Create and return function that increments the count
    for that key every time the method is called and returns
    the value returned by the original method
    Args:
        method (Callable): function to be wrapped
    Returns:
        A wrapper function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Increments `method` count and calls `method`
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


class Cache(object):
    """
    Implements caching using redis storage
    """
    def __init__(self) -> None:
        """
        Class instantiation method
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generate a random key (e.g. using uuid),
        store the input data in Redis using the random key and return the key
        Args:
            data: value to be stored against the generated key
        Returns:
            (str): the randomly generated key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        """
        Retrieves value of `key` from Redis storage
        """
        value = self._redis.get(key)
        return value if fn is None else fn(value)

    def get_str(self, key: str) -> str:
        """
        Calls get method with fn as a byte to string function
        Args:
            key (str): key to search for
        Returns:
            value (str): value mapped to the provide `key`
        """
        return self.get(key, lambda s: s.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Calls get method with fn as a byte to int function
        Args:
            key (str): key to search for
        Returns:
            value (int): value mapped to the provide `key`
        """
        return self.get(key, lambda n: int(n))


def replay(fn: Callable) -> None:
    """
    Display the history of calls of a particular function.
    Args:
        fn (Callable): a function whose history to display
    """
    display = ''
    fnName = fn.__qualname__
    ikey = '{}:inputs'.format(fn.__qualname__)
    okey = '{}:outputs'.format(fn.__qualname__)
    cache = redis.Redis()
    if not cache.exists(ikey):
        return
    display += '{} was called {} times:\n'.format(fnName, cache.llen(ikey))
    for i, o in zip(cache.lrange(ikey, 0, -1), cache.lrange(okey, 0, -1)):
        display += "{}(*{}) -> {}\n".format(
            fnName, i.decode('utf-8'), o.decode('utf-8'))
    print(display, end="")
