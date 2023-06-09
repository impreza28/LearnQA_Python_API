from requests import  Response
import json
class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_massage):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in Json Format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response Json doesn't have key '{name}'"
        assert response_as_dict[name] == expected_value, error_massage

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in Json Format. Response text is '{response.text}'"
        assert name in response_as_dict, f"Response Json doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in Json Format. Response text is '{response.text}'"
        for name in names:
            assert name in response_as_dict, f"Response Json doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_not_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in Json Format. Response text is '{response.text}'"
        for name in names:
            assert name is not response_as_dict, f"Response Json have key '{name}'"

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in Json Format. Response text is '{response.text}'"
        assert name  not in response_as_dict, f"Response Json shouldn't have key '{name}'. But it's present"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Статус код не равен {expected_status_code}. Статус код {response.status_code}"

    @staticmethod
    def assert_message(response: Response, expected_message):
        assert response.text == expected_message, \
            f"Ответ не равен {expected_message}. Ответ {response.text}"

    @staticmethod
    def assert_message_decode_utf_8(response: Response, expected_message):
        response_decode = response.content.decode("utf-8")
        assert response_decode == expected_message, \
            f"Ответ не равен '{expected_message}'. Ответ '{response_decode}'"

    @staticmethod
    def assert_equality(param1, param2):
        assert param1 == param2, f"'{param1}' не равен '{param2}'"



