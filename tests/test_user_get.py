import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase
import allure

@allure.epic("Get cases")
class TestUserGet(BaseCase):
    @allure.description("Тест на  получение данных пользователя без предварительной авторизации")
    def test_user_details_not_auth(self):
        response = requests.get("https://playground.learnqa.ru/api/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.description("Тест на  получение данных пользователя")
    def test_get_user_datails_auth_as_same_user(self):

        with allure.step('Шаг 1: авторизация под пользователем id=2'):
            data={'email':'vinkotov@example.com',
                  'password':'1234'}
            response1 = requests.post("https://playground.learnqa.ru/api/user/login", data = data)

            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response1,"user_id")

        with allure.step('Шаг 2: получение данных пользователя и их проверка'):

            response2 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
                                     headers={"x-csrf-token":token}, cookies= {"auth_sid":auth_sid})
            expected_fiels = ["username", "email", "firstName", "lastName"]
            Assertions.assert_json_has_keys(response2, expected_fiels)

    # Ex16: Запрос данных другого пользователя
    @allure.description("Тест на получение данных другого пользователя")
    def test_get_datails_another_user(self):

        with allure.step('Шаг 1: авторизация под пользователем id=2'):
            data={'email':'vinkotov@example.com',
                  'password':'1234'}
            response1 = requests.post("https://playground.learnqa.ru/api/user/login", data = data)

            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")

        with allure.step('Шаг 2: получение данных пользователя и их проверка'):

            response2 = requests.get(f"https://playground.learnqa.ru/api/user/1",
                                     headers={"x-csrf-token":token}, cookies= {"auth_sid":auth_sid})
            Assertions.assert_json_has_key(response2, "username")
            check_fiels = ["email", "firstName", "lastName"]
            Assertions.assert_json_has_not_keys(response2, check_fiels)