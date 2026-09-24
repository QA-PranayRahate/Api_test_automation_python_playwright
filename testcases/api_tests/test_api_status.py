import allure
import pytest

from api_clients.status_api import StatusAPI

allure.story('check api status')


@pytest.mark.api
class TestApiStatus:
    ENDPOINT = '/status'

    with allure.step("check api status"):
        def test_api_status(self, api_request_context):
            status = StatusAPI(api_request_context)
            response = status.get_api_status()
            assert response.status == 200
            jsondata = response.json()
            print(jsondata.get('status'))


