#!/usr/bin/env python3
"""
Module exercise
"""
import redis
import uuid
from typing import Union


class Cache:
    """
    A class used to represent a Cache

    Attributes
    ----------
    data : str, bytes, int or float
        data to be stored in redis

    Methods
    -------
    store(data)
        takes a data argument and returns a randomly
        generated string key using uuid
    """
    def __init__(self) -> None:
        """ Initialize cache class"""
        self._redis = redis.Redis(host="localhost", port=6379, db=0)
        self._redis.flushdb

    def store(self, data: Union[str, bytes, int, float]) -> str:
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
