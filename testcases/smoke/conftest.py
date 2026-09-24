import pytest

from api_clients.cart_api import CartAPI
from api_clients.client_api import ClientAPI
from config import config
from testcases.api_tests.Test_api_client_authorization import fake


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


@pytest.fixture(scope='session')
def cart_id(api_request_context, access_token):
    cart_api = CartAPI(api_request_context)
    response = cart_api.create_cart(access_token)
    assert response.status == 201, f"Failed to create cart: {response.text()}"
    return response.json()['cartId']


def pytest_sessionfinish(session, exitstatus):
    """Keep Allure raw results in the results folder only."""
    if hasattr(session.config, "workerinput"):
        return

    print("\n--- Test session completed. Allure raw results saved in allure-results ---")
