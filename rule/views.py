from django.shortcuts import render
from django.http import JsonResponse
from bson import ObjectId

from utils.response_model import success_response, error_response
from utils.pymongo_api import db, find_all, insert_one, update_one, delete_one, replace_one, find_one


rule_template_collection = db['rule_template']
rule_collection = db['rule']
rule_group_collection = db['rule_group']
location_rule_group_collection = db['location_rule_group']


def get_all_rule_template(request):
    try:
        if request.method == 'GET':
            print(request)
            all_rule_templates = find_all(rule_template_collection)
            return JsonResponse(success_response(all_rule_templates))
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))
    
    
def get_rule_template(request):
    try:
        if request.method == 'GET':
            rule_template = request.GET.dict()
            rule_template_id = rule_template['id']
            rule_template = find_one(rule_template_collection, 
                       {
                           "_id": ObjectId(rule_template_id)
                       })
            return JsonResponse(success_response(rule_template))
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))
    
    
def add_rule_template(request):
    try:
        if request.method == 'POST':
            rule_template = request.POST.dict()
            _id = insert_one(rule_template_collection, rule_template)
            return JsonResponse(success_response({"id": str(_id.inserted_id)}))
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))
    
    
def update_rule_template(request):
    try:
        if request.method == 'POST':
            rule_template = request.POST.dict()
            rule_template_id = rule_template['id']
            update_one(rule_template_collection,
                       {
                           "_id": ObjectId(rule_template_id)
                       },
                       {
                           "name": rule_template['name'],
                           "description": rule_template['description'],
                           "params": rule_template['params']
                       })
            return JsonResponse(success_response())
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))
    

def delete_rule_template(request):
    try:
        if request.method == 'GET':
            rule_template = request.GET.dict()
            rule_template_id = rule_template['id']
            delete_one(rule_template_collection, 
                       {
                           "_id": ObjectId(rule_template_id)
                       })
            return JsonResponse(success_response())
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))
    
    
def get_all_rule(request):
    try:
        if request.method == 'GET':
            all_rules = find_all(rule_collection)
            return JsonResponse(success_response(all_rules))
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))
    

def get_rule(request):
    try:
        if request.method == 'GET':
            rule = request.GET.dict()
            rule_id = rule['id']
            rule = find_one(rule_collection, 
                       {
                           "_id": ObjectId(rule_id)
                       })
            return JsonResponse(success_response(rule))
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))
    
    
def add_rule(request):
    try:
        if request.method == 'POST':
            rule = request.POST.dict()
            _id = insert_one(rule_collection, rule)
            return JsonResponse(success_response({"id": str(_id.inserted_id)}))
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))
    
    
def update_rule(request):
    try:
        if request.method == 'POST':
            rule = request.POST.dict()
            rule_id = rule['id']
            update_one(rule_collection, 
                       {
                           "_id": ObjectId(rule_id)
                       },
                       {
                           "name": rule['name'],
                           "description": rule['description'],
                           "rule_template_id": rule['rule_template_id'],
                           "params": rule['params']
                       })
            return JsonResponse(success_response())
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))


def delete_rule(request):
    try:
        if request.method == 'GET':
            rule = request.GET.dict()
            rule_id = rule['id']
            delete_one(rule_collection, 
                       {
                           "_id": ObjectId(rule_id)
                       })
            return JsonResponse(success_response())
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))
    
    
def get_all_rule_group(request):
    try:
        if request.method == 'GET':
            all_rule_groups = find_all(rule_group_collection)
            return JsonResponse(success_response(all_rule_groups))
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))
    
    
def get_rule_group(request):
    try:
        if request.method == 'GET':
            rule_group = request.GET.dict()
            rule_group_id = rule_group['id']
            rule_group = find_one(rule_group_collection, 
                       {
                           "_id": ObjectId(rule_group_id)
                       })
            return JsonResponse(success_response(rule_group))
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))
    
    
def add_rule_group(request):
    try:
        if request.method == 'POST':
            rule_group = request.POST.dict()
            _id = insert_one(rule_group_collection, rule_group)
            return JsonResponse(success_response({"id": str(_id.inserted_id)}))
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))
    
    
def update_rule_group(request):
    try:
        if request.method == 'POST':
            rule_group = request.POST.dict()
            rule_group_id = rule_group['id']
            update_one(rule_group_collection,
                       {
                           "_id": ObjectId(rule_group_id)
                       },
                       {
                           "name": rule_group['name'],
                           "rules": rule_group['rules']
                       })
            return JsonResponse(success_response())
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))


def delete_rule_group(request):
    try:
        if request.method == 'GET':
            rule_group = request.GET.dict()
            rule_group_id = rule_group['id']
            delete_one(rule_group_collection, 
                       {
                           "_id": ObjectId(rule_group_id)
                       })
            return JsonResponse(success_response())
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))
    
    
def get_all_location_rule_group(request):
    try:
        if request.method == 'GET':
            all_location_rule_groups = find_all(location_rule_group_collection)
            return JsonResponse(success_response(all_location_rule_groups))
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))
    
    
def get_location_rule_group(request):
    try:
        if request.method == 'GET':
            location_rule_group = request.GET.dict()
            location_rule_group_id = location_rule_group['id']
            location_rule_group = find_one(location_rule_group_collection, 
                       {
                           "_id": ObjectId(location_rule_group_id)
                       })
            return JsonResponse(success_response(location_rule_group))
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))
    
    
def attach_rule_group_to_location(request):
    try:
        if request.method == 'POST':
            location_rule_group = request.POST.dict()
            location = location_rule_group['location']
            _id = replace_one(location_rule_group_collection,
                       {
                           "location": location
                       },
                       {
                           "location": location,
                           "rule_group_id": location_rule_group['rule_group_id']
                       })
            return JsonResponse(success_response({"id": str(_id.upserted_id)}))
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))


def detach_rule_group_from_location(request):
    try:
        if request.method == 'GET':
            location_rule_group = request.GET.dict()
            location_rule_group_id = location_rule_group['id']
            delete_one(location_rule_group_collection, 
                       {
                           "_id": ObjectId(location_rule_group_id)
                       })
            return JsonResponse(success_response())
    except Exception as error:
        print(error)
        return JsonResponse(error_response(error))