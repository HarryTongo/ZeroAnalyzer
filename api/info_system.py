import requests

from config import API_BASE_URL, INFO_SYSTEM_PARAMS

QUERY_TYPE = "site"


def fetch_info_system_data(query):
    # 设置请求参数
    params = INFO_SYSTEM_PARAMS.copy()  # 复制默认参数
    params["query"] = f'title=="{query}"||company={query}&&(status_code=200||status_code="")&&url=!""'
    # params["query"] = f'company={query}&&status_code=200&&url=!""'
    params["query_type"] = QUERY_TYPE

    response = requests.post(API_BASE_URL, json=params)

    return response.json()
