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
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Статус код не равен {expected_status_code}. Статус код {response.status_code}"

    @staticmethod
    def assert_message(response: Response, expected_message):
        assert response.text == expected_message, \
            f"Ответ не равен {expected_message}. Ответ {response.text}"