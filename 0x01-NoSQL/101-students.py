#!/usr/bin/env python3
""" 101-students """
from pymongo import MongoClient


def top_students(mongo_collection):
    """
    Arguments
    ---------
    mongo_collection : object
        collection object
    Returns
    --------
    List
        All students sorted by average score
    """
    for obj in mongo_collection.find():
        average = 0
        for o in obj["topics"]:
            average += o["score"]
        average /= len(obj["topics"])
        mongo_collection.update_one({"_id": obj["_id"]},
                                    {"$set": {"averageScore": average}})
    return list(mongo_collection.find().sort("averageScore", -1))
