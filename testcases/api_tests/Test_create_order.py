import json

import allure

from api_clients.order_api import OrderAPI
from testcases.api_tests.conftest import fake


class TestOrderAPI:

    with allure.step("Create Order API Test"):
        def test_create_order(self, api_request_context, access_token, cart_id):
            order_api = OrderAPI(api_request_context)
            response = order_api.create_order(
                access_token,
                cart_id,
                customer_name=fake.name(),
            )

            assert response.status == 201, (
                f"Expected 201, got {response.status}. Body: {response.text()}"
            )

            response_data = response.json()
            print(response_data)
            assert 'orderId' in response_data, f"No Order Id in response: {response_data}"
            assert response_data.get('created') is True

    with allure.step('get all products in the order'):
        def test_get_all_products(self, access_token, api_request_context, order_id):
            order_api = OrderAPI(api_request_context)
            response = order_api.get_all_orders(access_token)
            print(response.text)

            assert response.status == 200, (
                f"Expected {response.status}, got {response.status}. Body: {response.text()}"
            )
            response_data = response.json()

            assert isinstance(response_data, list), f"Expected a list, got: {type(response_data)}"
            assert len(response_data) > 0, "Expected at least one order, got an empty list"

            for order in response_data:
                assert 'id' in order, f"Missing id in order: {order}"
                assert 'items' in order, f"Missing items in order: {order}"
                assert len(order['items']) > 0, f"Order {order['id']} has no items"

                for item in order['items']:
                    assert 'quantity' in item, f"Missing quantity in item: {item}"
                    assert item['quantity'] > 0, f"Invalid quantity in item: {item}"

            quantity = response_data[0]['items'][0]['quantity']
            print(quantity)
            for data in response_data:
                print(json.dumps(data, indent=1))
