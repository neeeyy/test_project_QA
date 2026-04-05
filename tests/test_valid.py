import allure
import pytest
from data.payloads import valid_payloads_value


@allure.feature(
    "Валидные проверки работы с созданием и получением информации об объявлениях"
)
@allure.story("Создание объявление")
@allure.title("Создание объявления")
@allure.description("""
Создание объявления POST /api/1/item:
- Отправка валидного payload
- Проверка статус кода 200
- Проверка заголовка Content-Type = application/json
- Проверка наличия поля 'status' и его типа str
- Проверка, что POST запрос неидемпотентный -
    создаётся новое объявление при повторном запросе
""")
@pytest.mark.valid_create_item_post
def test_post_item(api, payload, allure_attach):
    response = api.create_item(payload)
    with allure.step("Проверяем статус код ответа"):
        assert response.status_code == 200, f"{response.status_code} должен быть 200"
    allure_attach(response.status_code, name="status code")
    allure_attach(response.json(), name="response json")
    allure_attach(payload, name="requests payload")
    data = response.json()
    with allure.step("Проверяем заголовки ответа"):
        headers = response.headers
        assert headers["Content-Type"] == "application/json"
    allure_attach(dict(headers), name="response headers")
    with allure.step('Проверяем наличие "status" в data'):
        assert "status" in data, f'нет поля "status" в {data}'
    with allure.step("Проверяем тип status"):
        assert isinstance(
            data["status"], str
        ), f"{response.status_code} должен быть str"
    with allure.step("Проверка иденпотентности"):
        response_post2 = api.create_item(payload)
        item_id_post1 = data["status"].split(" - ")[-1]
        data_post2 = response_post2.json()
        item_id_post2 = data_post2["status"].split(" - ")[-1]
        assert item_id_post1 != item_id_post2


@allure.feature(
    "Валидные проверки работы с созданием и получением информации об объявлениях"
)
@allure.story("Получение информации о объявлении по его идентификатору")
@allure.title("Запрос объявления по item_id")
@allure.description("""
Получение информации об объявлении GET /api/1/item/{item_id}:
- Отправка GET запроса с валидным item_id
- Проверка статус кода 200
- Проверка заголовка Content-Type = application/json
- Проверка, что поля JSON совпадают с отправленным payload
- Проверка идемпотентности запроса - повторный GET не изменяет данные
""")
@pytest.mark.valid_get_item_by_id
def test_get_item(api, item_id, payload, allure_attach):
    with allure.step("Получаем item_id в фикстуре и отправляем get по item_id"):
        response = api.get_item_id(item_id)
    with allure.step("Проверяем статус код ответа"):
        assert response.status_code == 200
    allure_attach(response.status_code, name="status code")
    allure_attach(payload, name="requests payload")
    get_data = response.json()
    allure_attach(get_data, name="response json")
    with allure.step(
        "проверем что get вернул поля с такими же значениями, как в payload"
    ):
        for item in get_data:
            assert item["statistics"]["likes"] == payload["statistics"]["likes"]
            assert item["statistics"]["viewCount"] == payload["statistics"]["viewCount"]
            assert item["statistics"]["contacts"] == payload["statistics"]["contacts"]
            assert item["sellerId"] == payload["sellerID"]
            assert item["name"] == payload["name"]
    with allure.step("Проверяем заголовки ответа"):
        headers = response.headers
        assert headers["Content-Type"] == "application/json"
    allure_attach(dict(headers), name="response headers")
    with allure.step("проверка иденпотентности"):
        response_get2 = api.get_item_id(item_id)
        assert get_data == response_get2.json()


@allure.feature(
    "Валидные проверки работы с созданием и получением информации об объявлениях"
)
@allure.story("Получение всех объявлений по id пользователя")
@allure.title("Все объявления по user_id")
@allure.description("""
Получение всех объявлений пользователя GET /api/1/user/{seller_id}/items:
- Отправка GET запроса с валидным seller_id
- Проверка статус кода 200
- Проверка, что созданное объявление присутствует в списке
- Проверка структуры и типов полей каждого объявления
- Проверка соответствия вложенных полей statistics payload
- Проверка заголовка Content-Type = application/json
- Проверка идемпотентности запроса повторный - GET не изменяет данные
""")
@pytest.mark.valid_get_items_by_user
def test_get_user_items(api, payload, allure_attach, item_id):
    user_id = payload["sellerID"]
    response = api.get_user_items(user_id)
    with allure.step("Проверяем статус код ответа"):
        assert response.status_code == 200
    allure_attach(response.status_code, name="status code")
    allure_attach(response.json(), name="response json")
    allure_attach(payload, name="requests payload")
    data = response.json()
    with allure.step("Проверяем, что созданное объявление есть у этого пользователя"):
        search_item_id = [i for i in data if i["id"] == item_id]
        assert search_item_id, f"созданное объявление {item_id} не найдено"
    with allure.step("Проверка структуры, значений и типов"):
        assert len(data) > 0, f"список пуст {len(data)}"
        for item in data:
            # cтруктура
            assert "sellerId" in item
            assert "name" in item
            assert "price" in item
            assert "statistics" in item
            stats = item["statistics"]
            assert "likes" in stats
            assert "viewCount" in stats
            assert "contacts" in stats
            # значения
            assert item["sellerId"] == user_id
            # типы
            assert isinstance(item["sellerId"], int)
            assert isinstance(item["name"], str)
            assert isinstance(item["price"], int)
            assert isinstance(stats, dict)
            assert isinstance(stats["likes"], int)
            assert isinstance(stats["viewCount"], int)
            assert isinstance(stats["contacts"], int)
    with allure.step("Проверка заголовков"):
        headers = response.headers
        assert headers["Content-Type"] == "application/json"
    allure_attach(dict(headers), name="response headers")
    with allure.step("Проверка иденпотентности"):
        response_items2 = api.get_user_items(user_id)
        assert response.json() == response_items2.json()


@allure.feature(
    "Валидные проверки работы с созданием и получением информации об объявлениях"
)
@allure.story("Получение статистики о объявлении по его идентификатору")
@allure.title("Получение статистики объявления по item_id")
@allure.description("""
Получение статистики по объявлению GET /api/2/statistic/{item_id}:
- Отправка GET запроса с валидным item_id
- Проверка статус кода 200
- Проверка заголовка Content-Type = application/json
- Проверка совпадения полей JSON со статистикой, указанной в payload
- Проверка идемпотентности запроса - повторный GET не изменяет данны
""")
@pytest.mark.valid_get_item_statistics
def test_item_statistics(api, item_id, payload, allure_attach):
    response = api.get_item_statistics(item_id)
    with allure.step("проверяем status code объявления"):
        assert response.status_code == 200
    allure_attach(response.status_code, name="status code")
    allure_attach(response.json(), name="response json")
    allure_attach(payload, name="requests payload")
    data = response.json()
    data_statistics = payload["statistics"]
    with allure.step(
        "проверем что get вернул поля с такими же значениями, как в payload"
    ):
        for item_data in data:
            assert data_statistics["contacts"] == item_data["contacts"]
            assert data_statistics["likes"] == item_data["likes"]
            assert data_statistics["viewCount"] == item_data["viewCount"]
    with allure.step("проверка заголовков"):
        headers = response.headers
        assert headers["Content-Type"] == "application/json"
    allure_attach(dict(headers), name="response headers")
    with allure.step("Проверка иденпотентности"):
        response_get2 = api.get_item_statistics(item_id)
        assert data == response_get2.json()


@allure.feature(
    "Проверки нижней границы значений + предположительно валидные большие значения"
)
@allure.story("Тестирование малых и больших значений")
@allure.description("""
- Отправить POST /api/1/item с payload valid_payloads
- Проверить статус код - 200
""")
@pytest.mark.valid_post_any_value
def test_valid_value(api, allure_attach, get_json):
    for payload in valid_payloads_value:
        response = api.create_item(payload)
        data = get_json(response)
        allure_attach(data, name="response json")
        allure_attach(response.status_code, name="response status_code")
        with allure.step("Проверяем статус код"):
            assert (
                response.status_code == 200
            ), f"передали {payload} и получили код {response.status_code}"
