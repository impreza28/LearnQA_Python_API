import requests
import allure
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase

@allure.epic("Edit cases")
class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        with allure.step('Шаг 1: создание пользователя'):
            # register
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)
            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            first_name = register_data['firstName']
            password = register_data['password']
            user_id = self.get_json_value(response1, "id")

        with allure.step('Шаг 2: авторизация под пользователем шага 1'):
        # login
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        with allure.step('Шаг 3: изменить firstName пользователя'):
            # edit
            new_name = "Changed Name"

            response3 = MyRequests.put(f"/user/{user_id}", data={"firstName": new_name}, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

            Assertions.assert_code_status(response3, 200)

        with allure.step('Шаг 4: проверка firstName после изменения'):
            # get
            response4 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token},
                                     cookies = {"auth_sid": auth_sid})
            #response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
            #                         headers={"x-csrf-token": token},
            #                         cookies={"auth_sid": auth_sid})
            Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Неверное имя после редактирования")

    # Попытаемся изменить данные пользователя, будучи неавторизованными
    @allure.description("Тест на изменение данных пользователя без предварительной авторизации")
    def test_edit_user_without_auth(self):
        with allure.step('Шаг 1: создать пользователя'):
    # Шаг 1: создать пользователя

            register_data = self.prepare_registration_data()
            response1 = MyRequests.post(f"/user/", data=register_data)
            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            first_name = register_data['firstName']
            password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        with allure.step('Шаг 2: попытка изменить раннее созданного пользователя без авторизации'):
        # Шаг 2: попытка изменить раннее созданного пользователя без авторизации
            new_first_name = "Changed Name"
            new_password = "changed_password"
            new_email = "changed_email@example.com"

            response2 = MyRequests.put(f"/user/{user_id}", data=
            {
                "firstName": new_first_name,
                "password": new_password,
                "email": new_email
            })

            Assertions.assert_code_status(response2, 400)
            expected_message = "Auth token not supplied"
            Assertions.assert_message_decode_utf_8(response2, expected_message)

        with allure.step('Шаг 3: авторизация под пользователем из шага 1'):
        # Шаг 3: авторизация под пользователем из шага 1

            data = \
                {
                    'email': email,
                    'password': password
                }
            response3 = MyRequests.post("/user/login", data=data)
            Assertions.assert_code_status(response3, 200)

            auth_sid = self.get_cookie(response3, "auth_sid")
            token = self.get_header(response3, "x-csrf-token")

        with allure.step('Шаг 4: проверить данные пользователя, которого пытались изменить'):

        # Шаг 4: проверить данные пользователя, которого пытались изменить

            response4 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid})

            Assertions.assert_code_status(response4, 200)
            Assertions.assert_json_value_by_name(response4, "firstName", first_name, "Неверный firstName после редактирования")
            Assertions.assert_json_value_by_name(response4, "email", email, "Неверный email после редактирования")

# - Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    @allure.description("Тест на изменение данных пользователя при авторизации другим пользователем")
    def test_edit_user_under_different_user(self):
        with allure.step('Шаг 1: создать пользователя'):
        # Шаг 1: создать пользователя

            register_data = self.prepare_registration_data()

            response1 = MyRequests.post("/user/", data=register_data)
            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            first_name = register_data['firstName']
            password = register_data['password']
            user_id = self.get_json_value(response1, "id")

        with allure.step('Шаг 2: авторизация под другим пользователем'):

        # Шаг 2: авторизация под другим пользователем
            data = {'email': 'vinkotov@example.com',
                    'password': '1234'}

            response2 = MyRequests.post("/user/login", data=data)
            Assertions.assert_code_status(response2, 200)

        with allure.step('Шаг 3: изменить данные созданного пользователя из шага 1'):
        # Шаг 3: изменить данные созданного пользователя из шага 1
            new_first_name = "Changed Name"
            new_password = "changed_password"
            new_email = "changed_email@example.com"

            response3 = MyRequests.put(f"/user/{user_id}", data=
            {
                "firstName": new_first_name,
                "password": new_password,
                "email": new_email
            })

            Assertions.assert_code_status(response3, 400)
            expected_message = "Auth token not supplied"
            Assertions.assert_message_decode_utf_8(response3, expected_message)

        with allure.step('Шаг 4: авторизация под пользователем из шага 1'):

        # Шаг 4: авторизация под пользователем из шага 1
            data = {'email': email,
                    'password': password}

            response2 = MyRequests.post("/user/login", data=data)
            Assertions.assert_code_status(response2, 200)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        with allure.step('Шаг 5: получение информации о пользователе, которого хотели изменить'):

        # Шаг 5: получение информации о пользователе, которого хотели изменить

            response4 = MyRequests. get(f"/user/{user_id}", headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid})
            Assertions.assert_code_status(response4, 200)
            Assertions.assert_json_value_by_name(response4, "firstName", first_name,
                                                 "Неверный firstName после редактирования")
            Assertions.assert_json_value_by_name(response4, "email", email, "Неверный email после редактирования")

# - Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    @allure.description("Тест на изменение Email пользователя без символа @")
    def test_edit_user_with_incorrect_email(self):
        with allure.step('Шаг 1: создать пользователя'):
        # Шаг 1: создать пользователя

            register_data = self.prepare_registration_data()

            response1 = MyRequests.post("/user/", data=register_data)
            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            first_name = register_data['firstName']
            password = register_data['password']
            user_id = self.get_json_value(response1, "id")

        with allure.step('Шаг 2: авторизация пользователем'):

        # Шаг 2: авторизация пользователем
            data = {'email': email,
                    'password': password}

            response2 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")
            Assertions.assert_code_status(response2, 200)

        with allure.step('Шаг 3: изменить данные созданного пользователя из шага 1'):

        # Шаг 3: изменить данные созданного пользователя из шага 1

            new_email = "changed_emailexample.com"

            response3 =MyRequests. put(f"/user/{user_id}", headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid},
                                     data={"email": new_email})

            Assertions.assert_code_status(response3, 400)
            expected_message='Invalid email format'
            Assertions.assert_message_decode_utf_8(response3, expected_message)

        with allure.step('Шаг 4: получение информации о пользователе, которого хотели изменить'):

        # Шаг 4: получение информации о пользователе, которого хотели изменить
            response4 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid})
            Assertions.assert_code_status(response4, 200)
            Assertions.assert_json_value_by_name(response4, "email", email,
                                                 "Неверный email после редактирования")

    @allure.description("Тест на изменение firstName пользователя на значение в один символ")
# - Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    def test_edit_user_with_incorrect_firstName(self):

        with allure.step('Шаг 1: создать пользователя'):
            # Шаг 1: создать пользователя

            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)
            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            first_name = register_data['firstName']
            password = register_data['password']
            user_id = self.get_json_value(response1, "id")

        with allure.step('Шаг 2: авторизация пользователем'):

            # Шаг 2: авторизация пользователем
            data = {'email': email,
                    'password': password}
            response2 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")
            Assertions.assert_code_status(response2, 200)

        with allure.step('Шаг 3: изменить данные созданного пользователя из шага 1'):

            # Шаг 3: изменить данные созданного пользователя из шага 1

            new_first_name = "a"
            response3 = MyRequests.put(f"/user/{user_id}", data={"firstName": new_first_name}, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

            Assertions.assert_code_status(response3, 400)
            Assertions.assert_json_has_key(response3, "error")
            expected_message = "Too short value for field firstName"
            Assertions.assert_equality(response3.json()["error"], expected_message)

        with allure.step('Шаг 4: получение информации о пользователе, которого хотели изменить'):

            # Шаг 4: получение информации о пользователе, которого хотели изменить

            response4 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

            Assertions.assert_code_status(response4, 200)
            Assertions.assert_json_value_by_name(response4, "firstName", first_name,
                                                 "Неверный firstName после редактирования")