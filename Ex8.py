import requests
import time
import json

    ### 1) создавал задачу

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
responseJson = response.json()
print(f'Запуск создания задачи...')
token = responseJson["token"]
seconds = responseJson["seconds"]
print(f'Cоздана задача {responseJson["token"]}')

    ### 2) делал один запрос с token ДО того, как задача готова, убеждался в правильности поля status

responseStatus = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params = {"token":token})
responseJson = responseStatus.json()
print(f'Повторная отправка запроса по токену {token} ...')

if responseJson["status"] == 'Job is NOT ready':

    ### 3) ждал нужное количество секунд с помощью функции time.sleep()
    time.sleep(seconds)
else: print(f'Ошика при повторной отправке запроса по токену {token}')

    ### 4) делал бы один запрос c token ПОСЛЕ того, как задача готова, убеждался в правильности поля status и наличии поля result

responseStatus = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params = {"token":token})
responseJson = responseStatus.json()


if responseJson["status"] == 'Job is ready' and responseJson["result"] != '':
    print(f'Успешно создана задача: {responseJson["result"]}','\n', f'Статус задачи: {responseJson["status"]}')




