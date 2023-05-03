import pytest
import json
import requests

class TestEx12:
    def test_ex_12(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        header = response.headers.get("x-secret-homework-header")
        print(header)

        expected_header = 'Some secret value'
        assert header == expected_header, "Значение header в ответе != Some secret value"

