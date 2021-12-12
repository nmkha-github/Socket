import json

x = {
    'name': 'lê hoài'
}
search_result = json.dumps(x, ensure_ascii=False)
print(type(search_result))
