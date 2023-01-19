#!/usr/bin/env python3
"""
Module exercise
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps
UnionOfTypes = Union[bytes, float, str, int]


def replay(method: Callable):
    """display the history of calls of a particular function."""
    client = redis.Redis()
    key = method.__qualname__
    value = client.get(key)
    try:
        value = int(value.decode("utf-8"))
    except Exception:
        value = 0
    print(f"{key} was called {value} times:")
    inputs = client.lrange(f"{key}:inputs", 0, -1)
    outputs = client.lrange(f"{key}:outputs", 0, -1)
    for inp, outp in zip(inputs, outputs):
        try:
            inp = inp.decode("utf-8")
        except Exception:
            inp = ""
        try:
            outp = outp.decode("utf-8")
        except Exception:
            outp = ""
        print(f"{key}(*{inp}) -> {outp}")


def call_history(method: Callable) -> Callable:
    """
    Parameters
    ---------
    method : Callable
        a function to be decorated by count_calls

    Returns
    ---------
    Callable
      add its input parameters to one list in redis,
      and store its output into another list
    """
    @wraps(method)
    def wrapper_function(self, *args, **kwargs):
        inputs = f"{method.__qualname__}:inputs"
        outputs = f"{method.__qualname__}:outputs"
        output = method(self, *args, **kwargs)
        self._redis.rpush(inputs, str(args))
        self._redis.rpush(outputs, output)
        return output
    return wrapper_function


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

    @call_history
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
