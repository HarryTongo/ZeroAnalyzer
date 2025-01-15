import requests

'''
python 调用 0.zone api（信息系统）示例
'''

data = {
    "query": "company=北京大学",
    "query_type": "domain",
    "page": 1,
    "pagesize": 100,
    "zone_key_id": "9b80698597d3b481f4d2a49f484efc8d"
}

res = requests.post('https://0.zone/api/data/', json=data)

print(res.json())
