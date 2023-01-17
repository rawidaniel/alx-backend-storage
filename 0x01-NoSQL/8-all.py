#!/usr/bin/env python3
""" 8-all """


def list_all(mongo_collection):
    """
    Arguments
    ---------
    mongo_collection : object
        collection object
    Returns
    -------
    list
        list of documents or empty list if no document present in collection
    """
    if mongo_collection is None:
        return []
    return list(mongo_collection.find({}))
