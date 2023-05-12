import requests
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase


class TestUserDelete(BaseCase):

# Первый - на попытку удалить пользователя по ID 2.
    def test_delete_user_2(self):

    # Шаг 1: авторизация под пользователем id = 2
        data = \
            {
            'email': 'vinkotov@example.com',
            'password': '1234'
            }
        response1 = MyRequests.post("/user/login", data=data)
        Assertions.assert_code_status(response1, 200)
        user_id = response1.json()["user_id"]

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

    # Шаг 2: попытка удаления пользователя из шага 1
        response2 = MyRequests.delete(f"/user/{user_id}", cookies={"auth_sid": auth_sid}, headers= {"x-csrf-token": token})
        Assertions.assert_code_status(response2, 400)
        expected_message = 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.'
        Assertions.assert_message_decode_utf_8(response2, expected_message)

    # Шаг 3: проверить, что пользователь не удален

        response3 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 200)
        user_id = str(user_id)
        Assertions.assert_json_value_by_name(response3, "id", user_id, "Неверный id")

# Второй - позитивный. Создать пользователя, авторизоваться из-под него, удалить, затем попробовать получить его данные
# по ID и убедиться, что пользователь действительно удален.

    def test_delete_user(self):

    # Шаг 1: создать пользователя
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

    # Шаг 2: авторизоваться под пользователем шага 1

        data = {'email': email,
                'password': password}
        response2 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        Assertions.assert_code_status(response2, 200)

    # Шаг 3: удалить пользователя шага 1
        response3 = MyRequests.delete(f"/user/{user_id}", cookies={"auth_sid": auth_sid}, headers={"x-csrf-token": token})
        Assertions.assert_code_status(response3, 200)
        expected_message =''
        Assertions.assert_message_decode_utf_8(response3, expected_message)

    # Шаг 4: получить данные пользователя по ID и убедиться, что пользователь действительно удален
        response4 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response4, 404)
        expected_message='User not found'
        Assertions.assert_message_decode_utf_8(response4, expected_message)

# Третий - негативный, попробовать удалить пользователя, будучи авторизованными другим пользователем
    def test_delete_other_user(self):

        # Шаг 1: создать пользователя
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # Шаг 2: авторизоваться под другим пользователем

        data = {'email': 'vinkotov@example.com',
                'password': '1234'}
        response2 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        Assertions.assert_code_status(response2, 200)

        # Шаг 3: удалить пользователя шага 1
        response3 = MyRequests.delete(f"/user/{user_id}", cookies={"auth_sid": auth_sid},
                                      headers={"x-csrf-token": token})
        Assertions.assert_code_status(response3, 400)
        expected_message = 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.'
        Assertions.assert_message_decode_utf_8(response3, expected_message)

        # Шаг 4: получить данные пользователя по ID и убедиться, что пользователь действительно удален
        response4 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_value_by_name(response4, "username", "learnqa", "'username' пользователя не равен 'learnqa'")


