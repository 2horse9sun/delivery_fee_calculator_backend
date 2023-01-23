from django.test import TestCase
from django.test import Client
import json
from datetime import datetime

from . import calculate_function


class MinCartValueSurchargeTest(TestCase):
    def setUp(self):
        self.rule_params = {
            "min_cart_value": 1000
        }
        self.cart_value = 0
        self.delivery_distance = 0
        self.number_of_items = 0
        self.time = "2023-01-20T18:00:00Z"
        self.total_fee = 0

    def tearDown(self):
        pass

    def test_small_cart_value(self):
        self.cart_value = 0
        charge = calculate_function.min_cart_value_surcharge(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 1000)
        self.cart_value = 890
        charge = calculate_function.min_cart_value_surcharge(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 110)

    def test_large_cart_value(self):
        self.cart_value = 1000
        charge = calculate_function.min_cart_value_surcharge(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 0)
        self.cart_value = 1200
        charge = calculate_function.min_cart_value_surcharge(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 0)
        
        
class DistanceDifferentialChargeTest(TestCase):
    def setUp(self):
        self.rule_params = {
            "distance_threshold": 1000,
            "base_fee": 200,
            "additional_distance_step": 500,
            "additional_fee_per_step": 100
        }
        self.cart_value = 0
        self.delivery_distance = 0
        self.number_of_items = 0
        self.time = "2023-01-20T18:00:00Z"
        self.total_fee = 0

    def tearDown(self):
        pass

    def test_short_distance(self):
        self.delivery_distance = 0
        charge = calculate_function.distance_differential_charge(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 200)
        self.delivery_distance = 800
        charge = calculate_function.distance_differential_charge(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 200)

    def test_long_distance(self):
        self.delivery_distance = 1499
        charge = calculate_function.distance_differential_charge(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 300)
        self.delivery_distance = 1500
        charge = calculate_function.distance_differential_charge(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 300)
        self.delivery_distance = 1501
        charge = calculate_function.distance_differential_charge(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 400)
        self.delivery_distance = 4600
        charge = calculate_function.distance_differential_charge(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 1000)
        

class NumberOfItemsSurhargeTest(TestCase):
    def setUp(self):
        self.rule_params = {
            "number_of_items_threshold": 4,
            "additional_surcharge_per_extra_item": 50,
            "bulk_threshold": 12,
            "bulk_fee": 120
        }
        self.cart_value = 0
        self.delivery_distance = 0
        self.number_of_items = 0
        self.time = "2023-01-20T18:00:00Z"
        self.total_fee = 0

    def tearDown(self):
        pass

    def test_small_number(self):
        self.number_of_items = 0
        charge = calculate_function.number_of_items_surcharge(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 0)
        self.number_of_items = 4
        charge = calculate_function.number_of_items_surcharge(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 0)

    def test_large_number(self):
        self.number_of_items = 5
        charge = calculate_function.number_of_items_surcharge(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 50)
        self.number_of_items = 10
        charge = calculate_function.number_of_items_surcharge(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 300)

    def test_bulk_fee(self):
        self.number_of_items = 13
        charge = calculate_function.number_of_items_surcharge(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 570)
        self.number_of_items = 20
        charge = calculate_function.number_of_items_surcharge(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 920)


class MaxDeliveryFeeConstraintTest(TestCase):
    def setUp(self):
        self.rule_params = {
            "max_delivery_fee": 1500
        }
        self.cart_value = 0
        self.delivery_distance = 0
        self.number_of_items = 0
        self.time = "2023-01-20T18:00:00Z"
        self.total_fee = 0

    def tearDown(self):
        pass

    def test_small_delivery_fee(self):
        self.total_fee = 0
        charge = calculate_function.max_delivery_fee_constraint(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 0)
        self.total_fee = 1000
        charge = calculate_function.max_delivery_fee_constraint(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 0)

    def test_large_delivery_fee(self):
        self.total_fee = 1500
        charge = calculate_function.max_delivery_fee_constraint(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 0)
        self.total_fee = 2000
        charge = calculate_function.max_delivery_fee_constraint(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, -500)
        
class FreeDeliveryFeeConditionTest(TestCase):
    def setUp(self):
        self.rule_params = {
            "cart_value_threshold": 10000
        }
        self.cart_value = 0
        self.delivery_distance = 0
        self.number_of_items = 0
        self.time = "2023-01-20T18:00:00Z"
        self.total_fee = 0

    def tearDown(self):
        pass

    def test_small_cart_value(self):
        self.cart_value = 5000
        self.total_fee = 1500
        charge = calculate_function.free_delivery_fee_condition(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 0)
        self.cart_value = 8000
        self.total_fee = 1500
        charge = calculate_function.free_delivery_fee_condition(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, 0)

    def test_large_cart_value(self):
        self.cart_value = 10000
        self.total_fee = 1500
        charge = calculate_function.free_delivery_fee_condition(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, -1500)
        self.cart_value = 12000
        self.total_fee = 1500
        charge = calculate_function.free_delivery_fee_condition(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(charge, -1500)
        
        
class ExtraFeeDuringRushHourTest(TestCase):
    def setUp(self):
        self.rule_params = {
            "start_hour": 15,
            "end_hour": 19,
            "weekday": 4,
            "percentage": 20,
        }
        self.cart_value = 0
        self.delivery_distance = 0
        self.number_of_items = 0
        self.time = "2023-01-20T18:00:00Z"
        self.total_fee = 1000

    def tearDown(self):
        pass

    def test_rush_hour(self):
        self.time = datetime.fromisoformat("2023-01-19T18:00:00Z")
        charge = calculate_function.extra_fee_during_rush_hour(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(int(charge), 0)
        self.time = datetime.fromisoformat("2023-01-20T18:00:00Z")
        charge = calculate_function.extra_fee_during_rush_hour(self.rule_params, self.total_fee, self.cart_value, self.delivery_distance, self.number_of_items, self.time)
        self.assertEqual(int(charge), 200)
        
        
class DeliveryFeeCalculatorTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.rule_template_ids = []
        self.rule_ids = []
        self.rule_group_ids = []
        self.location_rule_group_ids = []
        
        min_cart_value_surcharge_template_id = self.client.post("/api/rule/add_rule_template/", {
            "name": "Mininum cart value surcharge",
            "description": "If the cart value is less than a threshold, a small order surcharge is added to the delivery price.\r\nAll the prices are represented in euro cents.",
            "function": "min_cart_value_surcharge",
            "params": "[{\"param_name\":\"min_cart_value\",\"type\":\"int\"}]"
        }).json()['data']['id']
        self.rule_template_ids.append(min_cart_value_surcharge_template_id)
        distance_differential_charge_template_id = self.client.post("/api/rule/add_rule_template/", {
            "name": "Differential pricing by delivery distance",
            "description": "Delivery fee is based on the range of delivery distance.\r\nAll the prices are represented in euro cents.",
            "function": "distance_differential_charge",
            "params": "[{\"param_name\":\"distance_threshold\",\"type\":\"int\"},{\"param_name\":\"base_fee\",\"type\":\"int\"},{\"param_name\":\"additional_distance_step\",\"type\":\"int\"},{\"param_name\":\"additional_fee_per_step\",\"type\":\"int\"}]"
        }).json()['data']['id']
        self.rule_template_ids.append(distance_differential_charge_template_id)
        number_of_items_surcharge_template_id = self.client.post("/api/rule/add_rule_template/", {
            "name": "Number of items surcharge",
            "description": "If the number of items is more than a threshold, an additional surcharge is added for each item above with possible bulk fee.\r\nAll the prices are represented in euro cents.",
            "function": "number_of_items_surcharge",
            "params": "[{\"param_name\":\"number_of_items_threshold\",\"type\":\"int\"},{\"param_name\":\"additional_surcharge_per_extra_item\",\"type\":\"int\"},{\"param_name\":\"bulk_threshold\",\"type\":\"int\"},{\"param_name\":\"bulk_fee\",\"type\":\"int\"}]"
        }).json()['data']['id']
        self.rule_template_ids.append(number_of_items_surcharge_template_id)
        max_delivery_fee_constraint_template_id = self.client.post("/api/rule/add_rule_template/", {
            "name": "Maximum delivery fee constraint",
            "description": "The total delivery fee has an upper bound.\r\nAll the prices are represented in euro cents.",
            "function": "max_delivery_fee_constraint",
            "params": "[{\"param_name\":\"max_delivery_fee\",\"type\":\"int\"}]"
        }).json()['data']['id']
        self.rule_template_ids.append(max_delivery_fee_constraint_template_id)
        free_delivery_fee_condition_template_id = self.client.post("/api/rule/add_rule_template/", {
            "name": "Free delivery fee condition",
            "description": "The delivery is free when the cart value reaches some threshold.\r\nAll the prices are represented in euro cents.",
            "function": "free_delivery_fee_condition",
            "params": "[{\"param_name\":\"cart_value_threshold\",\"type\":\"int\"}]"
        }).json()['data']['id']
        self.rule_template_ids.append(free_delivery_fee_condition_template_id)
        extra_fee_during_rush_hour_template_id = self.client.post("/api/rule/add_rule_template/", {
            "name": "Extra fee during rush hour",
            "description": "During the rush hour, the delivery fee (the total fee including possible surcharges) will be increased.\r\nstart_hour/end_hour: 0-24\r\nweekday: 0-6 (Monday-Sunday)\r\nAll the prices are represented in euro cents.",
            "function": "extra_fee_during_rush_hour",
            "params": "[{\"param_name\":\"start_hour\",\"type\":\"int\"},{\"param_name\":\"end_hour\",\"type\":\"int\"},{\"param_name\":\"weekday\",\"type\":\"int\"},{\"param_name\":\"percentage\",\"type\":\"int\"}]"
        }).json()['data']['id']
        self.rule_template_ids.append(extra_fee_during_rush_hour_template_id)
        
        min_cart_value_surcharge_rule_id = self.client.post("/api/rule/add_rule/", {
            "name": "Mininum cart value surcharge 2023",
            "description": "If the cart value is less than 10€, a small order surcharge is added to the delivery price. The surcharge is the difference between the cart value and 10€. For example if the cart value is 8.90€, the surcharge will be 1.10€.",
            "rule_template_id": min_cart_value_surcharge_template_id,
            "params": "[{\"param_name\":\"min_cart_value\",\"param_value\":\"1000\"}]"
        }).json()['data']['id']
        self.rule_ids.append(min_cart_value_surcharge_rule_id)
        distance_differential_charge_rule_id = self.client.post("/api/rule/add_rule/", {
            "name": "Differential pricing by delivery distance 2023",
            "description": "A delivery fee for the first 1000 meters (=1km) is 2€. If the delivery distance is longer than that, 1€ is added for every additional 500 meters that the courier needs to travel before reaching the destination. Even if the distance would be shorter than 500 meters, the minimum fee is always 1€.\r\nExample 1: If the delivery distance is 1499 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€\r\nExample 2: If the delivery distance is 1500 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€\r\nExample 3: If the delivery distance is 1501 meters, the delivery fee is: 2€ base fee + 1€ for the first 500 m + 1€ for the second 500 m => 4€",
            "rule_template_id": distance_differential_charge_template_id,
            "params": "[{\"param_name\":\"distance_threshold\",\"param_value\":\"1000\"},{\"param_name\":\"base_fee\",\"param_value\":\"200\"},{\"param_name\":\"additional_distance_step\",\"param_value\":\"500\"},{\"param_name\":\"additional_fee_per_step\",\"param_value\":\"100\"}]"
        }).json()['data']['id']
        self.rule_ids.append(distance_differential_charge_rule_id)
        number_of_items_surcharge_rule_id = self.client.post("/api/rule/add_rule/", {
            "name": "Number of items surcharge 2023",
            "description": "If the number of items is five or more, an additional 50 cent surcharge is added for each item above and including the fifth item. An extra \"bulk\" fee applies for more than 12 items of 1,20€\r\nExample 1: If the number of items is 4, no extra surcharge\r\nExample 2: If the number of items is 5, 50 cents surcharge is added\r\nExample 3: If the number of items is 10, 3€ surcharge (6 x 50 cents) is added\r\nExample 4: If the number of items is 13, 5,70€ surcharge is added ((9 * 50 cents) + 1,20€)",
            "rule_template_id":number_of_items_surcharge_template_id,
            "params": "[{\"param_name\":\"number_of_items_threshold\",\"param_value\":\"4\"},{\"param_name\":\"additional_surcharge_per_extra_item\",\"param_value\":\"50\"},{\"param_name\":\"bulk_threshold\",\"param_value\":\"12\"},{\"param_name\":\"bulk_fee\",\"param_value\":\"120\"}]"
        }).json()['data']['id']
        self.rule_ids.append(number_of_items_surcharge_rule_id)
        max_delivery_fee_constraint_rule_id = self.client.post("/api/rule/add_rule/", {
            "name": "Maximum delivery fee constraint 2023",
            "description": "The delivery fee can never be more than 15€, including possible surcharges.",
            "rule_template_id": max_delivery_fee_constraint_template_id,
            "params": "[{\"param_name\":\"max_delivery_fee\",\"param_value\":\"1500\"}]"
        }).json()['data']['id']
        self.rule_ids.append(max_delivery_fee_constraint_rule_id)
        free_delivery_fee_condition_rule_id = self.client.post("/api/rule/add_rule/", {
            "name": "Free delivery fee condition 2023",
            "description": "The delivery is free (0€) when the cart value is equal or more than 100€.",
            "rule_template_id": free_delivery_fee_condition_template_id,
            "params": "[{\"param_name\":\"cart_value_threshold\",\"param_value\":\"10000\"}]"
        }).json()['data']['id']
        self.rule_ids.append(free_delivery_fee_condition_rule_id)
        extra_fee_during_rush_hour_rule_id = self.client.post("/api/rule/add_rule/", {
            "name": "Extra fee during rush hour 2023",
            "description": "During the Friday rush (3 - 7 PM UTC), the delivery fee (the total fee including possible surcharges) will be multiplied by 1.2x. However, the fee still cannot be more than the max (15€).",
            "rule_template_id": extra_fee_during_rush_hour_template_id,
            "params": "[{\"param_name\":\"start_hour\",\"param_value\":\"15\"},{\"param_name\":\"end_hour\",\"param_value\":\"19\"},{\"param_name\":\"weekday\",\"param_value\":\"4\"},{\"param_name\":\"percentage\",\"param_value\":\"20\"}]"
        }).json()['data']['id']
        self.rule_ids.append(extra_fee_during_rush_hour_rule_id)
        
        rules = []
        rules.append({"rule_id": min_cart_value_surcharge_rule_id, "priority": 100})
        rules.append({"rule_id": distance_differential_charge_rule_id, "priority": 200})
        rules.append({"rule_id": number_of_items_surcharge_rule_id, "priority": 300})
        rules.append({"rule_id": extra_fee_during_rush_hour_rule_id, "priority": 400})
        rules.append({"rule_id": max_delivery_fee_constraint_rule_id, "priority": 500})
        rules.append({"rule_id": free_delivery_fee_condition_rule_id, "priority": 600})
        rules = json.dumps(rules)
        test_rule_group_id = self.client.post("/api/rule/add_rule_group/", {
            "name": "Helsinki 2023",
            "description": "Delivery fee calculation rules for Helsinki area in 2023",
            "rules": rules
        }).json()['data']['id']
        self.rule_group_ids.append(test_rule_group_id)
        
        test_location_rule_group_id = self.client.post("/api/rule/attach_rule_group_to_location/", {
            "location": "Helsinki",
            "rule_group_id": test_rule_group_id
        }).json()['data']['id']
        self.location_rule_group_ids.append(test_location_rule_group_id)
        

    def tearDown(self):
        for rule_template_id in self.rule_template_ids:
            self.client.get("/api/rule/delete_rule_template/", {"id": rule_template_id})
        for rule_id in self.rule_ids:
            self.client.get("/api/rule/delete_rule/", {"id": rule_id})
        for rule_group_id in self.rule_group_ids:
            self.client.get("/api/rule/delete_rule_group/", {"id": rule_group_id})
        for location_rule_group_id in self.location_rule_group_ids:
            self.client.get("/api/rule/detach_rule_group_from_location/", {"id": location_rule_group_id})


    def test_cart_value(self):
        total_fee = self.client.get("/api/calculation/calculate/", {
            "cart_value": "400",
            "delivery_distance": "500",
            "number_of_items": "4",
            "time": "2023-01-19T18:00:00Z",
            "location": "Helsinki"
        }).json()['data']['delivery_fee']
        self.assertEqual(total_fee, 800)
        total_fee = self.client.get("/api/calculation/calculate/", {
            "cart_value": "2000",
            "delivery_distance": "500",
            "number_of_items": "4",
            "time": "2023-01-19T18:00:00Z",
            "location": "Helsinki"
        }).json()['data']['delivery_fee']
        self.assertEqual(total_fee, 200)
        total_fee = self.client.get("/api/calculation/calculate/", {
            "cart_value": "12000",
            "delivery_distance": "500",
            "number_of_items": "4",
            "time": "2023-01-19T18:00:00Z",
            "location": "Helsinki"
        }).json()['data']['delivery_fee']
        self.assertEqual(total_fee, 0)
        
        
    def test_delivery_distance(self):
        total_fee = self.client.get("/api/calculation/calculate/", {
            "cart_value": "400",
            "delivery_distance": "500",
            "number_of_items": "4",
            "time": "2023-01-19T18:00:00Z",
            "location": "Helsinki"
        }).json()['data']['delivery_fee']
        
        self.assertEqual(total_fee, 800)
        total_fee = self.client.get("/api/calculation/calculate/", {
            "cart_value": "400",
            "delivery_distance": "1400",
            "number_of_items": "4",
            "time": "2023-01-19T18:00:00Z",
            "location": "Helsinki"
        }).json()['data']['delivery_fee']
        self.assertEqual(total_fee, 900)
        total_fee = self.client.get("/api/calculation/calculate/", {
            "cart_value": "400",
            "delivery_distance": "1600",
            "number_of_items": "4",
            "time": "2023-01-19T18:00:00Z",
            "location": "Helsinki"
        }).json()['data']['delivery_fee']
        self.assertEqual(total_fee, 1000)
        
        
    def test_number_of_items(self):
        total_fee = self.client.get("/api/calculation/calculate/", {
            "cart_value": "400",
            "delivery_distance": "500",
            "number_of_items": "4",
            "time": "2023-01-19T18:00:00Z",
            "location": "Helsinki"
        }).json()['data']['delivery_fee']
        self.assertEqual(total_fee, 800)
        total_fee = self.client.get("/api/calculation/calculate/", {
            "cart_value": "400",
            "delivery_distance": "500",
            "number_of_items": "10",
            "time": "2023-01-19T18:00:00Z",
            "location": "Helsinki"
        }).json()['data']['delivery_fee']
        self.assertEqual(total_fee, 1100)
        total_fee = self.client.get("/api/calculation/calculate/", {
            "cart_value": "400",
            "delivery_distance": "500",
            "number_of_items": "15",
            "time": "2023-01-19T18:00:00Z",
            "location": "Helsinki"
        }).json()['data']['delivery_fee']
        self.assertEqual(total_fee, 1470)
        
        
    def test_rush_hour(self):
        total_fee = self.client.get("/api/calculation/calculate/", {
            "cart_value": "400",
            "delivery_distance": "500",
            "number_of_items": "4",
            "time": "2023-01-20T18:00:00Z",
            "location": "Helsinki"
        }).json()['data']['delivery_fee']
        self.assertEqual(total_fee, 960)
        total_fee = self.client.get("/api/calculation/calculate/", {
            "cart_value": "400",
            "delivery_distance": "500",
            "number_of_items": "15",
            "time": "2023-01-20T18:00:00Z",
            "location": "Helsinki"
        }).json()['data']['delivery_fee']
        self.assertEqual(total_fee, 1500)