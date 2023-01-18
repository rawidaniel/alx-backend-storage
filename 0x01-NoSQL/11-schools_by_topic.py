#!/usr/bin/env python3
""" 11-schools_by_topic """


def schools_by_topic(mongo_collection, topic):
    """
    Arguments
    ---------
    mongo_collection : object
        collection object
    topics: string
        topic searched
    """
    return list(mongo_collection.find({"topics": topic}))
