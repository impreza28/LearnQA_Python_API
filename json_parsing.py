import json

string_as_json = '{"name": 45}'

obj = json.loads(string_as_json)

key = "name"

if key in obj:
    print(obj[key])
else:
    print(f"Ключа {key} в Json нет")