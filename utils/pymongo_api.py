"""Helper functions for MongoDB connection and data manipulation.

Functions in this module connect MongoDB, and execute CRUD commands.
Neccesary data formatting is also done here.

"""


from pymongo import MongoClient
from django.conf import settings
from bson import json_util
import json


client = MongoClient(host = settings.DB_HOSTNAME,
                    port = int(settings.DB_PORT)
                    )
db = client[settings.DB_NAME]


def object2json(data):
    return json.loads(json_util.dumps(data))


def find_format(item):
    item['id'] = item['_id']['$oid']
    item.pop('_id', None)
    return item


def find_one(collection, query):
    result = collection.find_one(query)
    if result != None:
        return find_format(object2json(collection.find_one(query)))
    else:
        return None


def find(collection, query):
    return list(map(find_format, object2json(list(collection.find(query)))))


def find_all(collection):
    return list(map(find_format, object2json(list(collection.find()))))


def insert_one(collection, dict):
    return collection.insert_one(dict)


def replace_one(collection, query, value, upsert = True):
    return collection.replace_one(query, value, upsert)


def update_one(collection, query, value):
    return collection.update_one(query, {"$set": value})


def delete_one(collection, query):
    return collection.delete_one(query)