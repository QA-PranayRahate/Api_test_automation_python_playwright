from unittest import TestCase

import allure
import pytest
from playwright.async_api import expect

from api_clients.product_api import ProductAPI

@allure.story('Test All Products API endpoint')
@pytest.mark.api
class TestProductAPI:

    with allure.step('Fetch all products'):
        def test_products(self,api_request_context):
            products = ProductAPI(api_request_context)
            response=products.get_products()
            assert response.status == 200, (response.status, response.text())
            jsondata=response.json()
            for data in jsondata:
                print(data)

    with allure.step('Verify Products not in Stock'):
        def test_products_not_in_stock(self, api_request_context):
            products = ProductAPI(api_request_context)
            response=products.get_product_not_in_stock()
            jsondata=response.json()
            for data in jsondata:
                if not data['inStock']:
                    print(data)

    with allure.step('Fetch products with id'):
        def test_get_product_by_id(self, api_request_context):
            products = ProductAPI(api_request_context)
            response=products.get_product_by_id('2177')
            jsondata=response.json()
            print(jsondata)
            assert response.status == 200, (response.status, response.text())
            assert jsondata.get('name') == 'Cosco Three Step Steel Platform'

    with allure.step("Fetch Products with Name"):
        def test_get_product_by_name(self, api_request_context):
            products = ProductAPI(api_request_context)
            response=products.get_product_by_name('French Bread')
            jsondata=response.json()
            print(jsondata)
            assert response.status == 200, (response.status, response.text())

            matching_product = next((p for p in jsondata if p['name'] == 'French Bread'), None)
            assert matching_product is not None, f"No product named 'French Bread' found in response: {jsondata}"
            assert matching_product['id'] == int('3486')