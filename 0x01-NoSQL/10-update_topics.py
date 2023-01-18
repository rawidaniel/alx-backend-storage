#!/usr/bin/env python3
""" 10-update_topics """


def update_topics(mongo_collection, name, topics):
    """
    Arguments
    ---------
    mongo_collection : object
        collection object
    name : string
        school name to update
    topics: list
        list of topics approached in the school
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
