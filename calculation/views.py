from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import json

from utils.response_model import success_response, error_response
from . import calculate_function
import utils.cache as cache


def find_rules(location):
    location_rule_group = cache.get_location_rule_group_by_location(location)

    if location_rule_group == None:
        return []
    
    # Each location is attached a rule group
    rule_group = cache.get_rule_group_by_id(location_rule_group['rule_group_id'])
    
    # Each rule group has several rules with different priorities
    rules = json.loads(rule_group['rules'])
    rules = sorted(rules, key = lambda rule: rule['priority'])
    
    # Map each rule to the associated fee calculation function
    for i, rule in enumerate(rules):
        rules[i] = cache.get_rule_by_id(rule['rule_id'])
        rules[i]['function'] = cache.get_rule_template_by_id(rules[i]['rule_template_id'])['function']
        rules[i]['rule_template_name'] = cache.get_rule_template_by_id(rules[i]['rule_template_id'])['name']
    return rules


def calculate_delivery_fee(request):
    if request.method == 'GET':
        delivery_info = request.GET.dict()
        cart_value = int(delivery_info['cart_value'])
        delivery_distance = int(delivery_info['delivery_distance'])
        number_of_items = int(delivery_info['number_of_items'])
        time = datetime.fromisoformat(delivery_info['time'])
        # Assume that different locations follow different delivery fee rules for simplicity. 
        # In production, many other factors could determine the rules.
        location = delivery_info['location']
        

        
        # Find all rules associated with the particular location
        rules = find_rules(location)
        total_fee = 0
        charge_info = []
        for rule in rules:
            # Every rule will trigger a function to calculate the partial charge for the delivery
            charge = calculate_function.calculate_function_map[rule['function']](rule['params'], total_fee, cart_value, delivery_distance, number_of_items, time)
            charge_info.append({
                "rule_template_name": rule['rule_template_name'],
                "charge": charge
            })
            total_fee += charge
        
        return JsonResponse(success_response({"delivery_fee": total_fee, "charge_info": charge_info}))
