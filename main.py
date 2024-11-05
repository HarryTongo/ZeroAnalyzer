import json
import os

import pandas as pd

from api.info_system import fetch_info_system_data
from api.mobile_apps import fetch_mobile_apps_data
from api.domains import fetch_domains_data
from api.emails import fetch_emails_data
from api.codes import fetch_codes_data
from api.personnels import fetch_personnels_data
from config import RAW_DATA_DIR, excel_output_file
from data_to_excel import info_system_data_converter, mobile_apps_data_converter, domains_data_converter, \
    emails_data_converter, codes_data_converter, personnels_data_converter


def save_data_to_json(data: dict, api_name: str, user_input: str):
    # 创建目录路径
    directory_name = os.path.join(RAW_DATA_DIR, user_input)  # 根据用户输入的内容创建
    json_file_name = f"{api_name}.json"  # 根据 API名称创建
    json_file_path = os.path.join(directory_name, json_file_name)  # 完整的json文件路径

    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    # 存储获取的数据为json文件
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(api_name + "扫描完成.......................")

def main():
    # 获取用户输入
    query = input("请输入要查询的内容:")


    # 调用 API 获取数据
    print(f"正在获取'{query}'的信息.......")
    print("+" * 100)

    # 获取data数据
    data_info_system = fetch_info_system_data(query)
    data_mobile_apps = fetch_mobile_apps_data(query)
    data_domains = fetch_domains_data(query)
    data_emails = fetch_emails_data(query)
    data_code = fetch_codes_data(query)
    data_personnels = fetch_personnels_data(query)

    # 存储json文件到data中
    save_data_to_json(data_info_system, "info_system", query)
    save_data_to_json(data_mobile_apps, "mobile_apps", query)
    save_data_to_json(data_domains, "domains", query)
    save_data_to_json(data_emails, "emails", query)
    save_data_to_json(data_code, "codes", query)
    save_data_to_json(data_personnels, "personnels", query)

    # 存储excl结果到result
    EXCEL_OUTPUT_FILE = excel_output_file + query + ".xlsx"
    with pd.ExcelWriter(EXCEL_OUTPUT_FILE, engine='openpyxl') as writer:
        info_system_data_converter(data_info_system, writer)
        mobile_apps_data_converter(data_mobile_apps, writer)
        domains_data_converter(data_domains, writer)
        emails_data_converter(data_emails, writer)
        codes_data_converter(data_code, writer)
        personnels_data_converter(data_personnels, writer)


if __name__ == "__main__":
    main()
    # with open("data/中国电子信息产业集团有限公司/info_system.json", 'r', encoding="utf-8") as f:
    #     context = f.read()
    #     context = json.loads(context)
    #     context_size = context['data']
    #     size_count = len(context_size)
    #     print(size_count)
