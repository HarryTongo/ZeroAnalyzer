import requests

from config import API_BASE_URL, INFO_SYSTEM_PARAMS

QUERY_TYPE = "code"


def fetch_codes_data(query):
    params = INFO_SYSTEM_PARAMS.copy()
    params['query'] = f"related_company=={query}||code_detail=={query}"
    params['query_type'] = QUERY_TYPE

    response = requests.post(API_BASE_URL, json=params)

    return response.json()
