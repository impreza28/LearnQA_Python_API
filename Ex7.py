import json
import requests

endStr = '----------------------'

### 1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
response1 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print('Пункт №1:', '\n', 'Ответ метода:', response1.text, '\n', 'Код ответа:', response1.status_code, '\n', endStr)

### 2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
response2 = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "HEAD"})
print('Пункт №2:', '\n', 'Ответ метода:', response2.text, '\n', 'Код ответа:', response2.status_code, '\n', endStr)

### 3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
# POST
response3POST = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "POST"})
print('Пункт №3.1:', '\n', 'Ответ метода POST:', response3POST.text, '\n', 'Код ответа:', response3POST.status_code,
      '\n', endStr)
# GET
response3GET = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": "GET"})
print('Пункт №3.2:', '\n', 'Ответ метода GET:', response3GET.text, '\n', 'Код ответа:', response3GET.status_code, '\n',
      endStr)
# PUT
response3PUT = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "PUT"})
print('Пункт №3.3:', '\n', 'Ответ метода PUT:', response3PUT.text, '\n', 'Код ответа:', response3PUT.status_code, '\n',
      endStr)
# DELETE
response3DELETE = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type",
                                  data={"method": "DELETE"})
print('Пункт №3.4:', '\n', 'Ответ метода DELETE:', response3DELETE.text, '\n', 'Код ответа:',
      response3DELETE.status_code, '\n', endStr)

# 4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.

methods = [{"method": "GET"}, {"method": "POST"}, {"method": "PUT"}, {"method": "DELETE"}]
print('Пункт №4:')
for i in methods:
    result = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=i)
    if result.text == '{"success":"!"}' and i != {"method": "GET"}:
        print(f"Метод GET с params = {i} имеет ответ: {result.text} и Код ответа: {result.status_code}")
    elif result.text != '{"success":"!"}' and i == {"method": "GET"}:
        print(f"Метод GET с params = {i} имеет ответ: {result.text} и Код ответа: {result.status_code}")

    result = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", data=i)
    if result.text == '{"success":"!"}':
        print(f"Метод GET с data = {i} имеет ответ: {result.text} и Код ответа: {result.status_code}")

    result = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=i)
    if result.text == '{"success":"!"}' and i != {"method": "POST"}:
        print(f"Метод POST с data = {i} имеет ответ: {result.text} и Код ответа: {result.status_code}")
    elif result.text != '{"success":"!"}' and i == {"method": "POST"}:
        print(f"Метод POST с data = {i} имеет ответ: {result.text} и Код ответа: {result.status_code}")


    result = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", params=i)
    if result.text == '{"success":"!"}':
        print(f"Метод POST с params = {i} имеет ответ: {result.text} и Код ответа: {result.status_code}")

    result = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=i)
    if result.text != '{"success":"!"}' and i == {"method": "PUT"}:
        print(f"Метод PUT с data = {i} имеет ответ: {result.text} и Код ответа: {result.status_code}")
    elif result.text == '{"success":"!"}' and i != {"method": "PUT"}:
        print(f"Метод PUT с data = {i} имеет ответ: {result.text} и Код ответа: {result.status_code}")

    result = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", params=i)
    if result.text == '{"success":"!"}':
        print(f"Метод PUT с params = {i} имеет ответ: {result.text} и Код ответа: {result.status_code}")

    result = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=i)
    if result.text != '{"success":"!"}' and i == {"method": "DELETE"}:
        print(f"Метод DELETE с data = {i} имеет ответ: {result.text} и Код ответа: {result.status_code}")
    elif result.text == '{"success":"!"}' and i != {"method": "DELETE"}:
        print(f"Метод DELETE с data = {i} имеет ответ: {result.text} и Код ответа: {result.status_code}")

    result = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", params=i)
    if result.text == '{"success":"!"}':
        print(f"Метод DELETE с params = {i} имеет ответ: {result.text} и Код ответа: {result.status_code}")

print(endStr)