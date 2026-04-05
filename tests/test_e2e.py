import allure
import requests


@allure.feature("E2E тест от создания до удаления объявления")
@allure.description("""
1. Post запрос на создание объявления
2. Get запрос для получения информации об объявлении
3. Get запрос для получения статистики об объявлении
4. Get запрос для получения всех объявления пользователя
5. Delete запрос для удаления объявления
""")
def test_e2e(api, payload, allure_attach):
    with allure.step(
        "Создаем объявление, проверяем статус код, получаем item_id и user_id"
    ):
        response_post = api.create_item(payload)
        assert (
            response_post.status_code == 200
        ), f"post code {response_post.status_code}, ожидали 200"
        allure_attach(response_post.status_code, name="response_post status code")
        data = response_post.json()
        allure_attach(data, name="response_post JSON")
        item_id = data["status"].split(" - ")[-1]
        user_id = payload["sellerID"]
    with allure.step(
        "Получаем информацию о объявлении по item_id и проверяем статус код"
    ):
        response_get_item = api.get_item_id(item_id)
        allure_attach(
            response_get_item.status_code, name="response_get_item status code"
        )
        assert (
            response_get_item.status_code == 200
        ), f"get code {response_get_item.status_code}, ожидали 200"
        allure_attach(response_get_item.json(), name="response_get_item JSON")
    with allure.step(
        "Получаем статистику по объявлению по item_id и проверяем статус код"
    ):
        response_get_statistics = api.get_item_statistics(item_id)
        allure_attach(
            response_get_statistics.status_code,
            name="response_get_statistics status code",
        )
        assert (
            response_get_statistics.status_code == 200
        ), f"get code {response_get_statistics}, ожидали 200"
        allure_attach(
            response_get_statistics.json(), name="response_get_statistics JSON"
        )
    with allure.step("Получаем все объявления пользователя по user_id"):
        response_get_items_by_user = api.get_user_items(user_id)
        allure_attach(
            response_get_items_by_user.status_code,
            name="response_get_items_by_users status code",
        )
        assert (
            response_get_items_by_user.status_code == 200
        ), f"get code {response_get_items_by_user}, ожидали 200"
        allure_attach(
            response_get_items_by_user.json(), name="response_get_items_by_users JSON"
        )
    with allure.step("удаляем объявление по item_id и проверяем корректность удаления"):
        response_delete = requests.delete(
            f"https://qa-internship.avito.com/api/2/item/{item_id}"
        )
        allure_attach(response_delete.status_code, name="response_delete status code")
        assert (
            response_delete.status_code == 200
        ), f"delete code {response_delete.status_code}, ожидали 200"
        response_get_item_after_del = api.get_item_id(item_id)
        allure_attach(
            response_get_item_after_del.status_code,
            name="response_get_item_after_del status code",
        )
        assert (
            response_get_item_after_del.status_code == 404
        ), f"get code {response_get_item_after_del}, ожидали 404"
