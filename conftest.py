import pytest
from copy import deepcopy
from api.main_class import Api
from data.payloads import valid_payload
import allure
import json


@pytest.fixture
def baseurl():
    return "https://qa-internship.avito.com"


@pytest.fixture
def api(baseurl):
    return Api(baseurl)


@pytest.fixture
def payload():
    return deepcopy(valid_payload)


@pytest.fixture
def item_id(api, baseurl, payload):
    response = api.create_item(payload)
    data = response.json()
    item_id = data["status"].split(" - ")[-1]
    return item_id


@pytest.fixture
def allure_attach():
    def attach(data, name="name"):
        if isinstance(data, (int, float, str)):
            allure.attach(
                str(data), name=name, attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                json.dumps(data, ensure_ascii=False, indent=2),
                name=name,
                attachment_type=allure.attachment_type.JSON,
            )

    return attach


@pytest.fixture
def get_json():
    def json(response):
        try:
            return response.json()
        except ValueError:
            return None

    return json
