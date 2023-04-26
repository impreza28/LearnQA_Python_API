import json
import requests

response = requests.get('https://playground.learnqa.ru/api/long_redirect')
history = response.history

print(f'Итоговый URL: {response.url}')
print(f'Количество редиректов: {(len(history))}')


