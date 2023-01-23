from pymongo import MongoClient
from bson import json_util
import json


client = MongoClient(host = "localhost", port = 27017)
db = client['delivery_fee_calculator']
rule_template_collection = db['rule_template']
rule_collection = db['rule']
rule_group_collection = db['rule_group']
location_rule_group_collection = db['location_rule_group']

print("Start to import...")

with open("rule_template.json", encoding='utf-8') as file:
    rule_template_json = json.load(file)
    for rule_template in rule_template_json:
        rule_template['_id'] = rule_template['_id']['$oid']
    print(rule_template_json)
    rule_template_collection.insert_many(rule_template_json)
    
with open("rule.json", encoding='utf-8') as file:
    rule_json = json.load(file)
    for rule in rule_json:
        rule['_id'] = rule['_id']['$oid']
    print(rule_json)
    rule_collection.insert_many(rule_json)
    
with open("rule_group.json", encoding='utf-8') as file:
    rule_group_json = json.load(file)
    for rule_group in rule_group_json:
        rule_group['_id'] = rule_group['_id']['$oid']
    print(rule_group_json)
    rule_group_collection.insert_many(rule_group_json)
    
with open("location_rule_group.json", encoding='utf-8') as file:
    location_rule_group_json = json.load(file)
    for location_rule_group in location_rule_group_json:
        location_rule_group['_id'] = location_rule_group['_id']['$oid']
    print(location_rule_group_json)
    location_rule_group_collection.insert_many(location_rule_group_json)

print("Successfully imported!")