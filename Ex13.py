import pytest
import json
import requests


class TestEx13:
    user_agents = [("Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"),
     ("Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1"),
    ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'),
    ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0'),
    ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1')]

    @pytest.mark.parametrize('user_agent', user_agents)
    def test_ex_13(self, user_agent):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        data = {"User-Agent": user_agent}

        response = requests.get(url, headers=data)

        # проверка ответа на наличие необходимых параметров
        assert "platform" in response.json()
        assert "browser" in response.json()
        assert "device" in response.json()

        #парсинг значений ответа
        actual_platform = response.json()["platform"]
        actual_browser = response.json()["browser"]
        actual_device = response.json()["device"]

        # 1. ============
        if data == {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'}:
            #ожидаемые значений
            expected_platform = 'Mobile'
            expected_browser = 'No'
            expected_device = 'Android'

            assert  actual_platform == expected_platform, f"Значение platform не равно {expected_platform}. В ответе получен {actual_platform} при data = 'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'"
            assert  actual_browser == expected_browser, f"Значение platform не равно {expected_browser}. В ответе получен {actual_browser} при data = 'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'"
            assert  actual_device == expected_device, f"Значение platform не равно {expected_device}. В ответе получен {actual_device} при data = 'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'"

        # 2. ============
        if data == {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'}:
            # ожидаемые значений
            expected_platform = 'Mobile'
            expected_browser = 'Chrome'
            expected_device = 'iOS'

            assert actual_platform == expected_platform, f"Значение platform не равно {expected_platform}. В ответе получен {actual_platform} при data = 'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'"
            assert actual_browser == expected_browser, f"Значение platform не равно {expected_browser}. В ответе получен {actual_browser} при data = 'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'"
            assert actual_device == expected_device, f"Значение platform не равно {expected_device}. В ответе получен {actual_device} при data = 'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'"

        # 3. ============
        if data == {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}:
            # ожидаемые значений
            expected_platform = 'Googlebot'
            expected_browser = 'Unknown'
            expected_device = 'Unknown'

            assert actual_platform == expected_platform, f"Значение platform не равно {expected_platform}. В ответе получен {actual_platform} при data = 'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'"
            assert actual_browser == expected_browser, f"Значение platform не равно {expected_browser}. В ответе получен {actual_browser} при data = 'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'"
            assert actual_device == expected_device, f"Значение platform не равно {expected_device}. В ответе получен {actual_device}  при data = 'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'"

        # 4. ============
        if data == {'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0'}:
            # ожидаемые значений
            expected_platform = 'Web'
            expected_browser = 'Chrome'
            expected_device = 'No'

            assert actual_platform == expected_platform, f"Значение platform не равно {expected_platform}. В ответе получен {actual_platform} при data = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0'"
            assert actual_browser == expected_browser, f"Значение platform не равно {expected_browser}. В ответе получен {actual_browser} при data = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0'"
            assert actual_device == expected_device, f"Значение platform не равно {expected_device}. В ответе получен {actual_device} при data = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0'"

        # 5. ============
        if data == {'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}:
            # ожидаемые значений
            expected_platform = 'Mobile'
            expected_browser = 'No'
            expected_device = 'iPhone'

            assert actual_platform == expected_platform, f"Значение platform не равно {expected_platform}. В ответе получен {actual_platform} при data = 'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'"
            assert actual_browser == expected_browser, f"Значение platform не равно {expected_browser}. В ответе получен {actual_browser} при data = 'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'"
            assert actual_device == expected_device, f"Значение platform не равно {expected_device}. В ответе получен {actual_device} при data = 'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'"





