"""Helper functions for Redis connection and cache store.

Functions in this module connect Redis, and store frequently accessed data into cache.

"""

import json
from django.core.cache import caches
from bson import json_util, ObjectId

from utils.pymongo_api import db, find_one


rule_template_collection = db['rule_template']
rule_collection = db['rule']
rule_group_collection = db['rule_group']
location_rule_group_collection = db['location_rule_group']
redis_cache = caches['default']


def get_location_rule_group_by_location(location):
    key = f'location_rule_group-{location}'
    location_rule_group = redis_cache.get(key)
    if(location_rule_group == None):
        location_rule_group = find_one(location_rule_group_collection, {"location": location})
        if location_rule_group != None:
            redis_cache.set(key, json.dumps(location_rule_group))
    else:
        location_rule_group = json.loads(location_rule_group)
    return location_rule_group


def get_rule_group_by_id(rule_group_id):
    key = f'rule_group-{rule_group_id}'
    rule_group = redis_cache.get(key)
    if(rule_group == None):
        rule_group = find_one(rule_group_collection, {"_id": ObjectId(rule_group_id)})
        if rule_group != None:
            redis_cache.set(key, json.dumps(rule_group))
    else:
        rule_group = json.loads(rule_group)
    return rule_group


def get_rule_by_id(rule_id):
    key = f'rule-{rule_id}'
    rule = redis_cache.get(key)
    if(rule == None):
        rule = find_one(rule_collection, {"_id": ObjectId(rule_id)})
        if rule != None:
            rule_params = {}
            for rule_param in json.loads(rule['params']):
                rule_params[rule_param['param_name']] = rule_param['param_value']
            rule['params'] = rule_params
            redis_cache.set(key, json.dumps(rule))
    else:
        rule = json.loads(rule)
    return rule


def get_rule_template_by_id(rule_template_id):
    key = f'rule-{rule_template_id}'
    rule_template = redis_cache.get(key)
    if(rule_template == None):
        rule_template = find_one(rule_template_collection, {"_id": ObjectId(rule_template_id)})
        if rule_template != None:
            redis_cache.set(key, json.dumps(rule_template))
    else:
        rule_template = json.loads(rule_template)
    return rule_template
        