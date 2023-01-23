"""Functions defined by rule templates for calculating partial charges.

Each function accepts common parameters as inputs:
    rule_params: rule-specific params used for calculation
    total_fee: accumulated total delivery fee before applying the current rule (integer, in euro cents)
    cart_value: sum of prices of all the items in customer's cart (integer, in euro cents)
    delivery_distance: distance a courier has to travel for delivery (integer, in meter)
    number_of_items: number of items in the cart
    time: ISO format time, python datetime object

Each function will return the partial charge for the associated rule. 

"""

import math


# Example
# If the cart value is less than 10€, a small order surcharge is added to the delivery price. 
# The surcharge is the difference between the cart value and 10€. 
# For example if the cart value is 8.90€, the surcharge will be 1.10€.
def min_cart_value_surcharge(rule_params, total_fee, cart_value, delivery_distance, number_of_items, time):
    min_cart_value = int(rule_params['min_cart_value'])
    charge = max(min_cart_value - cart_value, 0)
    return charge


# Example
# A delivery fee for the first 1000 meters (=1km) is 2€. If the delivery distance is longer than that, 1€ is added for every 
# additional 500 meters that the courier needs to travel before reaching the destination. 
# Even if the distance would be shorter than 500 meters, the minimum fee is always 1€.
# Example 1: If the delivery distance is 1499 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
# Example 2: If the delivery distance is 1500 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
# Example 3: If the delivery distance is 1501 meters, the delivery fee is: 2€ base fee + 1€ for the first 500 m + 1€ for the second 500 m => 4€
def distance_differential_charge(rule_params, total_fee, cart_value, delivery_distance, number_of_items, time):
    distance_threshold = int(rule_params['distance_threshold'])
    base_fee = int(rule_params['base_fee'])
    additional_distance_step = int(rule_params['additional_distance_step'])
    additional_fee_per_step = int(rule_params['additional_fee_per_step'])
    if delivery_distance <= distance_threshold:
        return base_fee
    else:
        charge = base_fee
        charge += math.ceil((delivery_distance - distance_threshold) / additional_distance_step) * additional_fee_per_step
        return charge
        

# Example
# If the number of items is five or more, an additional 50 cent surcharge is added for each item above five. 
# An extra "bulk" fee applies for more than 12 items of 1,20€
# Example 1: If the number of items is 4, no extra surcharge
# Example 2: If the number of items is 5, 50 cents surcharge is added
# Example 3: If the number of items is 10, 3€ surcharge (6 x 50 cents) is added
# Example 4: If the number of items is 13, 5,70€ surcharge is added ((9 * 50 cents) + 1,20€)
def number_of_items_surcharge(rule_params, total_fee, cart_value, delivery_distance, number_of_items, time):
    number_of_items_threshold = int(rule_params['number_of_items_threshold'])
    additional_surcharge_per_extra_item = int(rule_params['additional_surcharge_per_extra_item'])
    bulk_threshold = int(rule_params['bulk_threshold'])
    bulk_fee = int(rule_params['bulk_fee'])
    if number_of_items > number_of_items_threshold:
        charge = (number_of_items - number_of_items_threshold) * additional_surcharge_per_extra_item
        if number_of_items > bulk_threshold:
            charge += bulk_fee
        return charge
    else:
        return 0


# Example
# The delivery fee can never be more than 15€, including possible surcharges.
def max_delivery_fee_constraint(rule_params, total_fee, cart_value, delivery_distance, number_of_items, time):
    max_delivery_fee = int(rule_params['max_delivery_fee'])
    charge = min(max_delivery_fee - total_fee, 0)
    return charge


# Example
# The delivery is free (0€) when the cart value is equal or more than 100€.
def free_delivery_fee_condition(rule_params, total_fee, cart_value, delivery_distance, number_of_items, time):
    cart_value_threshold = int(rule_params['cart_value_threshold'])
    if cart_value >= cart_value_threshold:
        return -total_fee
    else:
        return 0


# Example
# During the Friday rush (3 - 7 PM UTC), the delivery fee (the total fee including possible surcharges) will be multiplied by 1.2x. 
# However, the fee still cannot be more than the max (15€).
def extra_fee_during_rush_hour(rule_params, total_fee, cart_value, delivery_distance, number_of_items, time):
    start_hour = int(rule_params['start_hour'])
    end_hour = int(rule_params['end_hour'])
    weekday = int(rule_params['weekday'])
    percentage = int(rule_params['percentage'])
    if(time.weekday() == weekday and time.hour >= start_hour and time.hour <= end_hour):
        return int(total_fee * percentage / 100)
    else:
        return 0
    
    
# Each rule template will trigger a function to calculate the partial charge for the delivery
calculate_function_map = {
    "min_cart_value_surcharge": min_cart_value_surcharge,
    "distance_differential_charge": distance_differential_charge,
    "number_of_items_surcharge": number_of_items_surcharge,
    "max_delivery_fee_constraint": max_delivery_fee_constraint,
    "free_delivery_fee_condition": free_delivery_fee_condition,
    "extra_fee_during_rush_hour": extra_fee_during_rush_hour
}