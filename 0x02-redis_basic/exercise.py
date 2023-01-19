#!/usr/bin/env python3
"""
Module exercise
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps
UnionOfTypes = Union[bytes, float, str, int]


def count_calls(method: Callable) -> Callable:
    """
    Parameters
    ---------
    method : Callable
        a function to be decorated by count_calls
    key : str
        value of the key
    Returns
    ---------
    Callable
      set a callable method name as key in redis and increment
      every time it called
    """
    key = method.__qualname__
    @wraps(method)
    def wrapper_function(self, *args, **kwargs):
        """ This is wrapper function for count_calls method """
        self._redis.incr(key)
        return method(self, *args, *kwargs)
    return wrapper_function


class Cache:
    """
    A class used to represent a Cache

    Attributes
    ----------
    data : str, bytes, int or float
        data to be stored in redis
    key : str
        value of the key
    fn : function
        function that convert byte string in to desired format

    Methods
    -------
    store(data)
        takes a data argument and returns a randomly
        generated string key using uuid
    get(key, fn)
        Reterive value corrsponding to key argument in deired format
    get_str(key)
        parametrize Cache.get with str function
    get_int(key)
        parametrize Cache.get with int function
    """
    def __init__(self) -> None:
        """ Initialize cache class"""
        self._redis = redis.Redis(host="localhost", port=6379, db=0)
        self._redis.flushdb()

    @count_calls
    def store(self, data: UnionOfTypes) -> str:
        """
        Parameters
        ----------
        data : str, bytes, int or float
            data to be stored in redis

        Returns
        -------
        str
            randomly generated key using uuid
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> UnionOfTypes:
        """
        Parameters
        ----------
        key : str
            value of the key
        fn : function
            function that convert byte string in to desired format

        Returns
        ---------
        Any
          value corrsponding to key argument in deired format
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Parameters
        ----------
        key : str
            value of the key
        Returns
        ---------
        str
          string value corrsponding to key
        """
        return self.get(key, str)

    def get_int(self, key: str) -> str:
        """
        Parameters
        ----------
        key : str
            value of the key
        Returns
        ---------
        int
          int value corrsponding to key
        """
        return self.get(key, int)
