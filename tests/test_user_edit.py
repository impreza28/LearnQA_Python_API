import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # register
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # edit
        new_name = "Changed Name"

        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name})
        Assertions.assert_code_status(response3, 200)

        # get
        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})
        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Неверное имя после редактирования")

    # Попытаемся изменить данные пользователя, будучи неавторизованными
    def test_edit_user_without_auth(self):
    # Шаг 1: создать пользователя

        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

    # Шаг 2: попытка изменить раннее созданного пользователя без авторизации
        new_first_name = "Changed Name"
        new_password = "changed_password"
        new_email = "changed_email@example.com"
        response2 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}", data=
        {
            "firstName": new_first_name,
            "password": new_password,
            "email": new_email
        })

        Assertions.assert_code_status(response2, 400)
        expected_message = "Auth token not supplied"
        Assertions.assert_message_decode_utf_8(response2, expected_message)

    # Шаг 3: авторизация под пользователем из шага 1

        data = \
            {
                'email': email,
                'password': password
            }
        response3 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        Assertions.assert_code_status(response3, 200)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

    # Шаг 4: проверить данные пользователя, которого пытались изменить

        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_value_by_name(response4, "firstName", first_name, "Неверный firstName после редактирования")
        Assertions.assert_json_value_by_name(response4, "email", email, "Неверный email после редактирования")

# - Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    def test_edit_user_under_different_user(self):
    # Шаг 1: создать пользователя

        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

    # Шаг 2: авторизация под другим пользователем
        data = {'email': 'vinkotov@example.com',
                'password': '1234'}
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        Assertions.assert_code_status(response2, 200)

    # Шаг 3: изменить данные созданного пользователя из шага 1
        new_first_name = "Changed Name"
        new_password = "changed_password"
        new_email = "changed_email@example.com"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}", data=
        {
            "firstName": new_first_name,
            "password": new_password,
            "email": new_email
        })

        Assertions.assert_code_status(response3, 400)
        expected_message = "Auth token not supplied"
        Assertions.assert_message_decode_utf_8(response3, expected_message)

    # Шаг 4: авторизация под пользователем из шага 1
        data = {'email': email,
                'password': password}
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        Assertions.assert_code_status(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

    # Шаг 5: получение информалии о пользователе, которого хотели изменить

        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_value_by_name(response4, "firstName", first_name,
                                             "Неверный firstName после редактирования")
        Assertions.assert_json_value_by_name(response4, "email", email, "Неверный email после редактирования")

# - Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    def test_edit_user_with_incorrect_email(self):

    # Шаг 1: создать пользователя

        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

    # Шаг 2: авторизация пользователем
        data = {'email': email,
                'password': password}
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        Assertions.assert_code_status(response2, 200)

    # Шаг 3: изменить данные созданного пользователя из шага 1

        new_email = "changed_emailexample.com"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",  headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"email": new_email})

        Assertions.assert_code_status(response3, 400)
        expected_message='Invalid email format'
        Assertions.assert_message_decode_utf_8(response3, expected_message)


    # Шаг 4: получение информации о пользователе, которого хотели изменить

        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_value_by_name(response4, "email", email,
                                             "Неверный email после редактирования")

# - Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    def test_edit_user_with_incorrect_firstName(self):
        # Шаг 1: создать пользователя

        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Шаг 2: авторизация пользователем
        data = {'email': email,
                'password': password}
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        Assertions.assert_code_status(response2, 200)

        # Шаг 3: изменить данные созданного пользователя из шага 1

        new_first_name = "a"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}", headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_first_name})

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_has_key(response3, "error")
        expected_message = "Too short value for field firstName"
        Assertions.assert_equality(response3.json()["error"], expected_message)

        # Шаг 4: получение информации о пользователе, которого хотели изменить

        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_value_by_name(response4, "firstName", first_name,
                                             "Неверный firstName после редактирования")


