import pytest
import allure
from data.payloads import (
    invalid_payloads_list,
    invalid_payloads,
    invalid_get_item_id_400,
    invalid_get_item_id_404,
    invalid_get_user_id,
    invalid_get_item_id,
    payload_field,
)


@allure.feature("Невалидные проверки создания и отображение информации об объявлениях")
@allure.story("Невалидные POST запросы")
@allure.title("POST запрос без одного из полей")
@allure.description("""
Проверка создания нового объявления через POST /api/1/item
    c отсутствующими полями в payload.
- Отправляем невалидный payload с отстствующими полями
- Проверяем статус код 400
- Проверяем структуру ответа, что есть ошибка об отсутствующие в payload полях
- Сравниваем статус код в теле ответа и HTTP
""")
@pytest.mark.parametrize("payload", invalid_payloads_list)
@pytest.mark.invalid_posts
def test_invalid_miss_json_post(api, payload, allure_attach, get_json):
    with allure.step("Отправляем запрос"):
        response = api.create_item(payload)
    with allure.step("Проверяем результат"):
        assert (
            response.status_code == 400
        ), f"показал {response.status_code} на {payload}"
    allure_attach(response.status_code, name="status code")
    allure_attach(payload, name="requests payload")
    missing_fields = [i for i in payload_field if i not in payload]
    data = get_json(response)
    if data:
        allure_attach(data, name="response json")
        with allure.step("Проверяем что отсутствующие поля упоминаются в теле ответа"):
            for field in missing_fields:
                assert (
                    field in data["result"]["message"]
                ), f"отсутсвует {field}, но в ответе: {data}"
        with allure.step(
            "Проверяем наличие поля status в теле ответа и тип поля status"
        ):
            assert "status" in data
            assert isinstance(data["status"], str)
        with allure.step(
            "Проверяем что код ошибке в теле ответа соответствует коду HTTP"
        ):
            assert response.status_code == int(
                data["status"]
            ), f"ищем {response.status_code} в {int(data['status'])}"
    else:
        allure_attach(
            response.text,
            name="response raw",
            attachment_type=allure.attachment_type.TEXT,
        )


@allure.feature("Невалидные проверки создания и отображение информации об объявлениях")
@allure.story("Невалидные POST запросы")
@allure.title("Невалидные значения в полях POST")
@allure.description("""
Проверка создания нового объявления через POST /api/1/item c невалидными данными.
- Отправляем невалидный payload c невалидными значениями
- Проверяем статус код 400
- Проверяем структуру ответа, наличе полей
""")
@pytest.mark.parametrize("payload", invalid_payloads)
@pytest.mark.invalid_posts_values
def test_post_invalid_value(api, payload, allure_attach, get_json):
    response = api.create_item(payload)
    allure_attach(payload, name="request payload")
    allure_attach(response.status_code, name="response status_code")
    data = get_json(response)
    if data:
        allure_attach(data, name="response data")
        with allure.step("проверям статус код"):
            assert (
                response.status_code == 400
            ), f"передано {payload}, получен ответ {response.status_code}"
        with allure.step("проверка наличия поля status в ответе и тип этого поля"):
            assert "status" in data
            assert isinstance(data["status"], str)
    else:
        allure_attach(
            response.text,
            name="response raw",
            attachment_type=allure.attachment_type.TEXT,
        )


@allure.feature("Невалидные проверки создания и отображение информации об объявлениях")
@allure.story("Невалидные Get запросы для получения объявления")
@allure.title("Невалидные item_id для получения объявления по идентификатору")
@allure.description("""
Проверка получения объявления через Get /api/1/item c невалидными данными в {id}.
- Отправляем запрос с невалидным {id}
- Проверяем статус код 400
- Проверяем наличие поля и его тип
- Сравниваем статус код в теле ответа и HTTP
""")
@pytest.mark.parametrize("item_id", invalid_get_item_id_400)
@pytest.mark.invalid_get_item_400
def test_invalid_get_item_id_400(api, item_id, allure_attach, get_json):
    response = api.get_item_id(item_id)
    allure_attach(response.status_code, name="status code")
    data = get_json(response)
    if data:
        allure_attach(data, name="response json")
        with allure.step("проверяем статус код"):
            assert response.status_code == 400
        with allure.step("проверям соответсвие кода в теле ответа к статус коду"):
            json_code = data.get("status") or data.get("code")
            assert isinstance(json_code, str) or isinstance(json_code, int)
            assert (
                int(json_code) == response.status_code
            ), f"в теле ответа код {int(json_code)}, HTTP код {response.status_code}"
    else:
        allure_attach(
            response.text,
            name="response raw",
            attachment_type=allure.attachment_type.TEXT,
        )


@allure.feature("Невалидные проверки создания и отображение информации об объявлениях")
@allure.story("Невалидные Get запросы для получения объявления")
@allure.title("Невалидные item_id для получения объявления по идентификатору")
@allure.description("""
Проверка получения объявления через Get /api/1/item c невалидными данными в {id}.
- Отправляем запрос с невалидным {id}
- Проверяем статус код 404
- Проверяем наличие поля и его тип
- Сравниваем статус код в теле ответа и HTTP
""")
@pytest.mark.parametrize("item_id", invalid_get_item_id_404)
@pytest.mark.invalid_get_item_404
def test_invalid_get_item_id_404(api, item_id, allure_attach, get_json):
    response = api.get_item_id(item_id)
    allure_attach(response.status_code, name="status code")
    data = get_json(response)
    if data:
        allure_attach(data, name="response json")
        with allure.step("проверяем статус код"):
            assert response.status_code == 404
        with allure.step("проверям соответсвие кода в теле ответа к статус коду"):
            json_code = data.get("code")
            assert isinstance(json_code, int)
            assert (
                int(json_code) == response.status_code
            ), f"в теле ответа код {int(json_code)}, HTTP код {response.status_code}"
    else:
        allure_attach(
            response.text,
            name="response raw",
            attachment_type=allure.attachment_type.TEXT,
        )


@allure.feature("Невалидные проверки создания и отображение информации об объявлениях")
@allure.story("Невалидные Get запросы для получения статистики объявления")
@allure.title("Невалидные item_id для получения статистики по объявлению")
@allure.description("""
Проверка получения статистики объявления через Get /api/2/statistic/
    c невалидными данными в {id}.
- Отправляем запрос с невалидным {id}
- Проверяем статус код 400 или 404
- Проверяем наличие поля и его тип
""")
@pytest.mark.parametrize("item_id", invalid_get_item_id)
@pytest.mark.invalid_get_item_statistics
def test_invalid_item_id_for_statistics(api, item_id, allure_attach, get_json):
    response = api.get_item_statistics(item_id)
    allure_attach(response.status_code, name="status code")
    data = get_json(response)
    if data:
        allure_attach(data, name="response json")
        with allure.step("проверяем статус код"):
            assert response.status_code in (400, 404)
        with allure.step("проверяем наличие строки message и её тип"):
            if "message" in data:
                assert isinstance(data["message"], str)
                assert isinstance(data["code"], int)
                assert (
                    response.status_code == data["code"]
                ), f'HTTP код {response.status_code}, в теле {data["code"]}'
            else:
                assert (
                    data["result"]["message"]
                    == "передан некорректный идентификатор объявления"
                )
                assert isinstance(data["result"]["message"], str)
                assert isinstance(data["status"], str)
                assert response.status_code == int(
                    data["status"]
                ), f'HTTP код {response.status_code}, в теле {int(data["status"])}'
    else:
        allure_attach(
            response.text,
            name="response raw",
            attachment_type=allure.attachment_type.TEXT,
        )


@allure.feature("Невалидные проверки создания и отображение информации об объявлениях")
@allure.story("Невалидные Get запросы для получения объявлений пользователя")
@allure.title("Невалидные seller_ID для запроса всех объявлений пользователя")
@allure.description("""
Проверка получения всех объявлений пользователя через Get /api/1/{seller_id}/item
    c невалидными данными в {seller_id}.
- Отправляем запрос с невалидным {seller_id}
- Проверяем статус код 400 или 404
- Проверяем наличие поля и его тип
""")
@pytest.mark.parametrize("seller_id", invalid_get_user_id)
@pytest.mark.invalid_get_user_items
@pytest.mark.xfail(
    reason="Баг: невалидный seller_id возвращает 200 вместо 400. Оформлено в BUGS-2"
)
def test_invalid_all_items_by_user_id(api, seller_id, allure_attach, get_json):
    response = api.get_user_items(seller_id)
    with allure.step("проверяем статус код"):
        assert response.status_code in (400, 404)
    allure_attach(response.status_code, name="status code")
    data = get_json(response)
    if data:
        allure_attach(data, name="response json")
        with allure.step("Проверяем наличие полей result и message в ответе и их тип"):
            if "result" in data:
                assert "message" in data["result"]
                assert isinstance(data["result"]["message"], str)
                assert isinstance(data["result"], dict)
            elif "message" in data:
                assert isinstance(data["message"], str)

    else:
        allure_attach(
            response.text,
            name="response raw",
            attachment_type=allure.attachment_type.TEXT,
        )
