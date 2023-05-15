import requests
import pytest
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]
    def setup(self):
        data = {'email': 'vinkotov@example.com',
                'password': '1234'
                }
        response1 = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(response1,"auth_sid")
        self.token = self.get_header(response1,"x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")
    @allure.description("Тест авторизации по емейлу и паролю")
    def test_auth_user(self):
        with allure.step('Шаг 1: Отправка запроса на авторизацию'):
            response2 = MyRequests.get("/user/auth", headers={"x-csrf-token": self.token}, cookies={"auth_sid": self.auth_sid})

        with allure.step('Шаг 2: Проверка наличия параметра user_id в ответе'):
            Assertions.assert_json_value_by_name(
                response2, "user_id",
                self.user_id_from_auth_method, "User id from auth method is not equal to user id from check mathod"
            )

    @allure.description("Тест на проверку статуса авторизации без отправки куки или хэдера")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_user(self, condition):

        if condition == "no_cookie":
            with allure.step('Шаг 1: Отправка запроса на авторизацию'):
                response2 = MyRequests.get("/user/auth", headers={"x-csrf-token": self.token})
        else:
            with allure.step('Шаг 1: Отправка запроса на авторизацию'):
                response2 = MyRequests.get("/user/aut", headers={"auth_sid": self.auth_sid})
        with allure.step('Шаг 2: Проверка наличия и значения параметра user_id в ответе'):
            Assertions.assert_json_value_by_name(
                response2, "user_id", 0, f"User is authorize with condition {condition}")
