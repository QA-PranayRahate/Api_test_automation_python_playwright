import allure
import pytest

from api_clients.cart_api import CartAPI


@allure.story('Create Cart API Test')
@pytest.mark.api
class TestCartAPI:
    with allure.step("Create Cart API Test"):
        def test_create_cart(self, api_request_context, access_token):
            cart_api = CartAPI(api_request_context)
            response = cart_api.create_cart(access_token=access_token)

            jsondata = response.json()
            print(response.status)
            print(jsondata.get('cartId'))

            assert response.status == 201, f'Cart Creation failed and got {response.status} and Body : {response.text()}'

    with allure.step("Add item to cart"):
        def test_add_item_to_cart(self, api_request_context, access_token,empty_cart):
            cart_api = CartAPI(api_request_context)
            product_id = 1710
            quantity = 1

            response = cart_api.add_item_to_cart(
                cart_id=empty_cart,
                access_token=access_token,
                product_id=product_id,
                quantity=quantity,
            )
            jsondata = response.json()

            assert response.status == 201, f'Product id {product_id} not available. Body: {response.text()}'
            print(f'product {product_id} added to cart {empty_cart} and quantity is {quantity}')
            print(jsondata)