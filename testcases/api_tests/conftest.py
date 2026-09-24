import os

import pytest
from faker import Faker

from api_clients.cart_api import CartAPI
from api_clients.client_api import ClientAPI
from api_clients.order_api import OrderAPI
from config import config

fake = Faker()


@pytest.fixture(scope='session')
def api_request_context(playwright):
    context = playwright.request.new_context(base_url=config.Config.BASE_URL)
    yield context
    context.dispose()


@pytest.fixture(scope='session')
def access_token(api_request_context):
    client_api = ClientAPI(api_request_context)
    response = client_api.register_client(
        name=fake.name(),
        email=fake.safe_email()
    )
    assert response.status == 201, f"Failed to register client: {response.text()}"
    return response.json()['accessToken']

@pytest.fixture(scope='function')
def empty_cart(api_request_context, access_token):
    """Empty cart, no item added — for tests exercising add-item itself."""
    cart_api = CartAPI(api_request_context)
    response = cart_api.create_cart(access_token)
    assert response.status == 201, f"Failed to create cart: {response.text()}"
    return response.json()['cartId']

@pytest.fixture(scope='function')
def cart_id(api_request_context, access_token,empty_cart,product_id):
    cart_api = CartAPI(api_request_context)
    response = cart_api.add_item_to_cart(access_token=access_token,
        cart_id=empty_cart,
        product_id=product_id,
        quantity=1)

    assert response.status == 201, f"Failed to create cart: {response.text()}"
    return empty_cart



@pytest.fixture(scope='function')
def order_id(api_request_context, access_token, cart_id, customer_name):
    order = OrderAPI(api_request_context)
    response = order.create_order(access_token, cart_id, customer_name)
    assert response.status == 201, f"Failed to create order: {response.text()}"
    return response.json()['orderId']


@pytest.fixture(scope='session')
def product_id():
    return 1710


@pytest.fixture(scope='function')
def customer_name():
    return fake.name()


import shutil
import subprocess


def pytest_sessionfinish(session, exitstatus):
    """Generate the Allure report and open it in the browser once tests finish."""
    if hasattr(session.config, "workerinput"):
        return  # skip in xdist worker processes, only run once on the main process

    print("\n--- Test session completed. Generating Allure report... ---")

    results_dir = "allure-results"
    output_dir = "allure-report"

    if not os.path.exists(results_dir):
        print(f"No '{results_dir}' folder found — nothing to generate.")
        return

    allure_cmd = shutil.which("allure")
    if not allure_cmd:
        print("Allure CLI not found on PATH. Install it or add it to PATH to auto-generate reports.")
        return

    try:
        os.makedirs(output_dir, exist_ok=True)
        result = subprocess.run(
            [allure_cmd, "generate", results_dir, "-o", output_dir, "--clean"],
            check=False,
            capture_output=True,
            text=True,
            shell=True,  # needed on Windows since allure is a .bat/.cmd wrapper
        )
        if result.returncode != 0:
            print(f"Allure generation failed:\n{result.stderr}")
            return

        print(f"Allure report generated at {output_dir}")

        # Auto-open the generated report in the default browser
        open_result = subprocess.run(
            [allure_cmd, "open", output_dir],
            check=False,
            shell=True,
        )
        if open_result.returncode != 0:
            print(f"Could not auto-open report — open it manually from: {output_dir}")

    except Exception as e:
        print(f"Could not generate/open Allure report: {e}")