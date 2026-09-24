# testcases/test_smoke_flow.py
import allure
import faker
import pytest

from api_clients.cart_api import CartAPI
from api_clients.client_api import ClientAPI
from api_clients.product_api import ProductAPI

fake = faker.Faker()


@allure.epic("Simple Grocery Store")
@allure.feature("End-to-End Flow")
@pytest.mark.smoke
class TestSmokeFlow:

    @allure.story("Full purchase journey")
    def test_end_to_end_grocery_flow(self, api_request_context):
        # Step 1: API is up
        with allure.step("Step 1: Check API status"):
            status_response = api_request_context.get("/status")
            assert status_response.status == 200, f"API status check failed: {status_response.text()}"
            jsondata = status_response.json()
            print('Step 1: API is up')
            print(jsondata, '\n')

        with allure.step("Step 2: Fetch product"):
            # Step 2: Products are available
            product_api = ProductAPI(api_request_context)
            all_products = product_api.get_products()
            products_response = product_api.get_product_by_id('1710')
            assert products_response.status == 200, f"Product fetch failed: {products_response.text()}"
            jsondata = all_products.json()

            print('Step 2: Products are available')

            for product in jsondata:
                print(product)

        with allure.step("Step 3: Register client and get access token"):
            # Step 3: Register client, get access token
            client_api = ClientAPI(api_request_context)
            client_response = client_api.register_client(
                name=fake.name(),
                email=fake.safe_email(),
            )
            assert client_response.status == 201, f"Client registration failed: {client_response.text()}"
            access_token = client_response.json()['accessToken']
            print('\n', 'Step 3: Client access token is valid')
            print(access_token, '\n')

        with allure.step("Step 4: Create cart"):
            # Step 4: Create a cart
            cart_api = CartAPI(api_request_context)
            cart_response = cart_api.create_cart(access_token)
            assert cart_response.status == 201, f"Cart creation failed: {cart_response.text()}"
            cart_id = cart_response.json()['cartId']
            print('Step 4: Cart Creted')
            print(cart_id, '\n')

        with allure.step("Step 5: Add item to cart"):
            # Step 5: Add item to that cart
            add_item_response = cart_api.add_item_to_cart(
                cart_id=cart_id,
                access_token=access_token,
                product_id=1710,
                quantity=1,
            )
            assert add_item_response.status == 201, f"Add item failed: {add_item_response.text()}"

            print(f"Smoke flow passed — token: {access_token}, cart: {cart_id}")
