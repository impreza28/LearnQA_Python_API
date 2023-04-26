import requests
from json.decoder import JSONDecodeError


response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)

try:
    parsedResponse = response.json()
    print(parsedResponse)
except JSONDecodeError:
    print("Response is not a JSON format")
