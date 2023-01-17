#!/usr/bin/env python3
""" 9-insert_school
"""


def insert_school(mongo_collection, **kwargs):
    """
    Arguments
    ---------
    mongo_collection : object
        collection object
    kwargs : dict
        key value pair data
    Returns
    -------
    object
        bson object id
    """
    if len(kwargs) == 0:
        return None
    return mongo_collection.insert_one(kwargs).inserted_id
