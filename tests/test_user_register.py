import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import datetime
from datetime import datetime
import allure

@allure.epic("Register cases")
class TestUserRegister(BaseCase):
    @allure.description("Тест на создание пользователя")
    def test_create_user_successfully(self):
        with allure.step('Шаг 1: создание пользователя'):

            data = self.prepare_registration_data()
            response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        with allure.step('Шаг 2: проверка статуса запроса (200)'):
            Assertions.assert_code_status(response, 200)

    @allure.description("Тест на создание пользователя с уже зарегистрированным Емейлом")
    def test_create_user_with_existing_email(self):

        with allure.step('Шаг 1: создание пользователя с уже зарегистрированным емейлом'):
            email = 'vinkotov@example.com'
            data = self.prepare_registration_data(email)

            response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        with allure.step('Шаг 2: проверка статуса и сообщения в ответе'):
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
                f"Ответ не равен Users with email {email} already exists. Ответ = {response.content}"

    @allure.description("Тест на создание пользователя с уже зарегистрированным Емейлом")
    def test_create_user_with_existing_email(self):

        with allure.step('Шаг 1: создание пользователя с уже зарегистрированным Емейлом'):
            email = 'vinkotov@example.com'
            data = {
                'password': '123',
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': email
            }
            response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        with allure.step('Шаг 2: проверка статуса и сообщения в ответе'):
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
                f"Ответ не равен Users with email {email} already exists. Ответ = {response.content}"

    # Создание пользователя с некорректным email - без символа @
    @allure.description("Тест на создание пользователя Емейлом без @")
    def test_create_user_with_incorrect_email(self):

        with allure.step('Шаг 1: Создание пользователя с некорректным email - без символа @'):
            email = 'vinkotovexample.com'
            data = {
                'password': '123',
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': email
            }
            response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        with allure.step('Шаг 2: проверка статуса и сообщения в ответе'):

            Assertions.assert_code_status(response, 400)
            assert response.text == "Invalid email format", \
                f"Ответ не равен 'Invalid email format'. Ответ = {response.text}"

    @allure.description("Тест на создание пользователя с username в 1 символ")
    # Создание пользователя с очень коротким именем в один символ
    def test_create_user_with_incorrect_username(self):

        with allure.step('Шаг 1: создание пользователя с username в 1 символ'):
            username = 'a'
            data = {
                'password': '123',
                'username': username,
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': 'vinkotov@example.com'
            }
            response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        with allure.step('Шаг 2: проверка статуса и сообщения в ответе'):
            Assertions.assert_code_status(response, 400)
            assert response.text == "The value of 'username' field is too short", \
                f"Ответ не равен 'The value of 'username' field is too short'. Ответ = {response.text}"

    # Создание пользователя с очень длинным именем - длиннее 250 символов
    @allure.description("Тест на создание пользователя с username в 250 символ")
    def test_create_user_with_username_more_250(self):

        with allure.step('Шаг 1: создание пользователя с username в 250 символ'):
            username = '11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111' \
                       '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111' \
                       '111111111111111111111111111111111111111111111111111'
            data = {
                'password': '123',
                'username': username,
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': 'vinkotov@example.com'
            }
            response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        with allure.step('Шаг 2: проверка статуса и сообщения в ответе'):
            Assertions.assert_code_status(response, 400)
            assert response.text == "The value of 'username' field is too long", \
                f"Ответ не равен 'The value of 'username' field is too long'. Ответ = {response.text}"

    # Создание пользователя без указания одного из полей - с помощью @parametrize необходимо проверить,
    # что отсутствие любого параметра не дает зарегистрировать пользователя

    dataRequests = [({
            'username': 'username',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        }),({
            'password': '123',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        }),({
            'password': '123',
            'username': 'username',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        }),({
            'password': '123',
            'username': 'username',
            'firstName': 'learnqa',
            'email': 'vinkotov@example.com'
        }),({
            'password': '123',
            'username': 'username',
            'firstName': 'learnqa',
            'lastName': 'learnqa'
        })]

    @allure.description("Тест на создание пользователя без параметров")
    @pytest.mark.parametrize('dataRequests', dataRequests)
    def test_create_user_without_parameter(self, dataRequests):

        with allure.step('Шаг 1: создание пользователя без параметров'):

            response = requests.post("https://playground.learnqa.ru/api/user/", data = dataRequests)

            Assertions.assert_code_status(response, 400)

        if dataRequests == {
            'username': 'username',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'}:
            with allure.step('Шаг 2: проверка сообщения'):

                expect_message = 'The following required params are missed: password'
                Assertions.assert_message(response, expect_message)

        if dataRequests == {
            'password': '123',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'}:

            with allure.step('Шаг 2: проверка сообщения'):

                expect_message = 'The following required params are missed: username'
                Assertions.assert_message(response, expect_message)

        if dataRequests == {
            'password': '123',
            'username': 'username',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'}:
            with allure.step('Шаг 2: проверка сообщения'):
                expect_message = 'The following required params are missed: firstName'
                Assertions.assert_message(response, expect_message)

        if dataRequests == {
            'password': '123',
            'username': 'username',
            'firstName': 'learnqa',
            'email': 'vinkotov@example.com'}:
            with allure.step('Шаг 2: проверка сообщения'):
                expect_message = 'The following required params are missed: lastName'
                Assertions.assert_message(response, expect_message)

        if dataRequests == {
            'password': '123',
            'username': 'username',
            'firstName': 'learnqa',
            'lastName': 'learnqa'}:
            with allure.step('Шаг 2: проверка сообщения'):
                expect_message = 'The following required params are missed: email'
                Assertions.assert_message(response, expect_message)