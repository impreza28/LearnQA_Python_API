import pytest
import json
import requests

class TestEx11:
    def test_ex_11(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookie = response.cookies.get("HomeWork")
        print(cookie)

        expected_cookie = 'hw_value'
        assert cookie == expected_cookie, "Значение cookie в ответе != hw_value"

