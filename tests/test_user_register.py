import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import datetime
from datetime import datetime


class TestUserRegister(BaseCase):
    def setup(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Ответ не равен Users with email {email} already exists. Ответ = {response.content}"

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Ответ не равен Users with email {email} already exists. Ответ = {response.content}"

    # Создание пользователя с некорректным email - без символа @
    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == "Invalid email format", \
            f"Ответ не равен 'Invalid email format'. Ответ = {response.text}"

    # Создание пользователя с очень коротким именем в один символ
    def test_create_user_with_incorrect_username(self):
        username = 'a'
        data = {
            'password': '123',
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == "The value of 'username' field is too short", \
            f"Ответ не равен 'The value of 'username' field is too short'. Ответ = {response.text}"

    # Создание пользователя с очень длинным именем - длиннее 250 символов
    def test_create_user_with_username_more_250(self):
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

        print(response.status_code)
        print(response.text)

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
    @pytest.mark.parametrize('dataRequests', dataRequests)
    def test_create_user_without_parameter(self, dataRequests):

        response = requests.post("https://playground.learnqa.ru/api/user/", data = dataRequests)

        Assertions.assert_code_status(response, 400)

        if dataRequests == {
            'username': 'username',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'}:

            expect_message = 'The following required params are missed: password'
            Assertions.assert_message(response, expect_message)

        if dataRequests == {
            'password': '123',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'}:

            expect_message = 'The following required params are missed: username'
            Assertions.assert_message(response, expect_message)

        if dataRequests == {
            'password': '123',
            'username': 'username',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'}:

            expect_message = 'The following required params are missed: firstName'
            Assertions.assert_message(response, expect_message)

        if dataRequests == {
            'password': '123',
            'username': 'username',
            'firstName': 'learnqa',
            'email': 'vinkotov@example.com'}:

            expect_message = 'The following required params are missed: lastName'
            Assertions.assert_message(response, expect_message)

        if dataRequests == {
            'password': '123',
            'username': 'username',
            'firstName': 'learnqa',
            'lastName': 'learnqa'}:

            expect_message = 'The following required params are missed: email'
            Assertions.assert_message(response, expect_message)