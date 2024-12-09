# 数据存储配置
RAW_DATA_DIR = "data/"

# Excel配置
excel_output_file = "result/"

# API配置
API_BASE_URL = "https://0.zone/api/data/"

# API key
ZONE_KEY_ID = ""

# API 接口参数(官方文档 https://0.zone/applyParticulars?type=site)
INFO_SYSTEM_PARAMS = {
    "query": "",
    "query_type": "",   # 搜索类型
    "page": 1,
    "pagesize": 100,
    "zone_key_id": ZONE_KEY_ID
}
