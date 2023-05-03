import requests
import pytest

class TestUserAuth:
    def test_auth_user(self):
        data = {'email':'vinkotov@example.com',
                'password':'1234'
                }

        responce1 = requests.post("https://playground.learnqa.ru/api/user/login", data = data)

        assert "auth_sid" in responce1.cookies, "не авторизованные куки в запросе"
        assert "x-csrf-token" in responce1.headers, "токен не в хедере"
        assert "user_id" in responce1.json(), "Нет user_id в ответе"

        auth_sid = responce1.cookies.get("auth_sid")
        token = responce1.headers.get("token")
        user_id_from_auth_method = responce1.json(["user_id"])

        responce2 = requests.get("https://playground.learnqa.ru/api/user/auth", headers={"x-csrf-token": token}, cookies={"auth_sid":auth_sid})
        assert "user_id" in responce2.json(), "Нет user_id в ответе"

        user_id_from_check_method = responce2.json()["user_id"]
        assert user_id_from_auth_method == user_id_from_check_method, "Юзер авторизации не равен юзеру логина"

