import os
from typing import Any, Callable

import bson
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

import Item.consts.consts as consts

def ensure_connection(func: Callable) -> Callable:
    def wrapper(self, *args, **kwargs):
        self._check_connection()
        return func(self, *args, **kwargs)
    return wrapper


class MongoDao:
    def __init__(self, db_name: str=consts.MONGO_TEST_DB, uri: str=None):
        if not uri:
            self.uri = os.environ.get("MONGODB_URI", "mongodb://mongodb:27010")
        else:
            self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None
        try:
            self._connect_to_db()
        except ConnectionFailure as e:
            raise

    def _connect_to_db(self):
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
        except ConnectionFailure as e:
            raise

    def _check_connection(self):
        try:
            self.client.admin.command('ping')
        except ConnectionFailure:
            self._connect_to_db()

    @ensure_connection
    def write_to_db(self, collection_name: str, data: Any) -> list[str]:
        collection = self.db[collection_name]
        if not isinstance(data, list):
            data = [data]
        result = collection.insert_many(data)

        # Return list of inserted ids as strings
        for i, _id in enumerate(result.inserted_ids):
            result.inserted_ids[i] = str(_id)

        return result.inserted_ids

    @ensure_connection
    def read_from_db(self, collection_name, query: dict, projection=None) -> list:
        """
        Retrieve documents based on query ignoring hidden documents.
        """
        if "_id" in query and not isinstance(query["_id"], bson.ObjectId):
            query["_id"] = bson.ObjectId(query["_id"])
        collection = self.db[collection_name]
        query = {**query, "hidden": {"$ne": True}}
        results = []
        for result in collection.find(query, projection):
            results.append(result)

        return list(results)

    @ensure_connection
    def update_db(self, collection_name, query: dict, update: Any, many=False) -> int:
        """
        Replace filtered documents with update.
        """
        if "_id" in query and not isinstance(query["_id"], bson.ObjectId):
            query["_id"] = bson.ObjectId(query["_id"])
        collection = self.db[collection_name]
        if many:
            result = collection.update_many(query, update)
        else:
            result = collection.update_one(query, update)
        return result.modified_count

    @ensure_connection
    def delete_from_db(self, collection_name: str, query: dict, many=False) -> int:
        """
        Hide (not actually delete) documents from a collection based on a query.
        """
        collection = self.db[collection_name]
        if many:
            result = collection.update_many(query, {"$set": {"hidden": True}})
        else:
            result = collection.update_one(query, {"$set": {"hidden": True}})
        return result.modified_count

    def close_connection(self):
        try:
            self.client.close()
        except ConnectionFailure:
            pass
