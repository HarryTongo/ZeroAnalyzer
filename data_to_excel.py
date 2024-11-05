import json

import pandas as pd


def adjust_column_widths(writer, sheet_name):
    # 获取当前活动列表
    worksheet = writer.sheets[sheet_name]

    # 遍历所有列并设置列宽
    for column in worksheet.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            if cell.value:
                # 计算实际长度，考虑到不同数据类型
                value_length = len(str(cell.value))
                if value_length > max_length:
                    max_length = value_length

        # 设置列宽，至少为一个预设值
        adjusted_width = (max_length + 2)  # 加上额外的空间
        adjusted_width = max(adjusted_width, 10)  # 设置最小宽度为 10
        worksheet.column_dimensions[column[0].column_letter].width = adjusted_width


def remove_illegal_characters(value):
    if isinstance(value, str):
        return ''.join(c for c in value if ord(c) >= 32)  # 只保留合法字符
    return value


def info_system_data_converter(data: dict, writer):
    if 'data' in data:
        if data['data']:
            # 只选择需要的字段
            info_fields = [
                'ip', 'port', 'url', 'title', 'os', 'ping', 'cms', 'banner_os', 'component', 'area', 'city',
                'continent', 'country', 'device_type', 'latitude', 'longitude', 'operator', 'province', 'service',
                'extra_info', 'app_name', 'banner', 'html_banner', 'group', 'company', 'tags', 'status_code',
                'beian', 'cname', 'ssl_certificate', 'icon_md5_base64', 'is_cdn', 'toplv_domain', 'timestamp'
            ]
            # 创建 DataFrame
            info_df = pd.DataFrame(data['data'])

            existing_info_fields = [field for field in info_fields if field in info_df.columns]

            info_df = info_df[existing_info_fields]

            info_df.rename(columns={
                'ip': 'ip',
                'port': '端口',
                'url': '链接',
                'title': '标题',
                'os': '操作系统',
                'ping': '查看服务器是否连通，通为1，反之为0',
                'cms': 'CMS',
                'banner_os': 'banner_os',
                'component': '组件',
                'area': '地区',
                'city': '城市',
                'continent': '洲',
                'country': '国家',
                'device_type': '设备类型',
                'latitude': '维度',
                'longitude': '经度',
                'operator': '运营商',
                'province': '省份',
                'service': '服务',
                'extra_info': '设备分类',
                'app_name': '应用名称',
                'banner': '端口的返回信息',
                'html_banner': 'HTML返回信息',
                'group': '团体',
                'company': '公司名称',
                'tags': '标签',
                'status_code': '状态码',
                'beian': '备案号',
                'cname': '网站cname分析',
                'ssl_certificate': 'SSL/TLS 证书下载地址',
                'icon_md5_base64': '网站icon列表(md5 + icon地址)',
                'is_cdn': '是否是CDN, 0: 否、1: 是',
                'toplv_domain': '顶级域名',
                'timestamp': '创建时间'
            }, inplace=True)

            ssl_info_list = []  # 创建一个列表来收集所有的 SSL 信息
            for item in data['data']:
                ssl_info = item.get('ssl_info', {})
                if ssl_info:
                    ssl_info_list.append(ssl_info)
            ssl_info_fields = ['issuer_cn', 'issuer_org', 'subject_cn', 'subject_org', 'detail']
            ssl_info_df = pd.DataFrame(ssl_info_list)
            existing_info_fields2 = [field for field in ssl_info_fields if field in ssl_info_df.columns]

            # 根据存在的字段筛选 DataFrame
            ssl_info_df = ssl_info_df[existing_info_fields2]
            ssl_info_df.rename(columns={
                'issuer_cn': 'SSL颁发者',
                'issuer_org': 'SSL颁发机构',
                'subject_cn': 'SSL通用名',
                'subject_org': 'SSL关联组织',
                'detail': 'SSL证书详情',
            }, inplace=True)
            combined_df = pd.concat([info_df, ssl_info_df], axis=1)
            combined_df = combined_df.apply(lambda col: col.apply(remove_illegal_characters))
            combined_df.to_excel(writer, sheet_name='信息系统', index=False)

            adjust_column_widths(writer, '信息系统')


def mobile_apps_data_converter(data: dict, writer):
    if 'data' in data:
        if data['data']:
            apps_fields = [
                'title', 'company', 'timestamp_update', 'type', 'icp', 'check_time'
            ]
            apps_df = pd.DataFrame(data['data'])
            existing_apps_fields = [field for field in apps_fields if field in apps_df.columns]
            apps_df = apps_df[existing_apps_fields]
            apps_df.rename(columns={
                'title': '应用名称',
                'company': '所属公司',
                'timestamp_update': '更新时间',
                'type': '应用类型',
                'icp': '备案号',
                'check_time': '备案时间',
            }, inplace=True)

            msg_list = []
            for item in data['data']:
                msg_info = item.get('msg', {})
                if msg_info:
                    msg_list.append(msg_info)

            msg_fields = [
                'app_id', 'wechat_fakeid', 'iconUrl', 'introduction', 'service_type', 'code', 'app_url',
                'ext_information'
            ]
            msg_df = pd.DataFrame(msg_list)
            existing_apps_fields2 = [field for field in msg_fields if field in msg_df.columns]
            msg_df = msg_df[existing_apps_fields2]
            msg_df.rename(columns={
                'app_id': '小程序',
                'wechat_fakeid': '应用类型为微信公众号时表示',
                'iconUrl': '应用图标地址',
                'introduction': '应用描述',
                'service_type': '公众号的类型',
                'code': '公众号二维码地址',
                'app_url': 'app 的下载地址',
                'ext_information': '数据来源其他原始信息，附加信息',
            }, inplace=True)
            combined_df = pd.concat([apps_df, msg_df], axis=1)
            combined_df = combined_df.apply(lambda col: col.apply(remove_illegal_characters))
            combined_df.to_excel(writer, sheet_name="移动端应用", index=False)

            adjust_column_widths(writer, "移动端应用")


def domains_data_converter(data: dict, writer):
    if 'data' in data:
        if data['data']:
            domains_df = pd.DataFrame(data['data'])

            domains_fields = [
                'company', 'domain', 'icp', 'toplv_domain', 'url'
            ]
            existing_domains_fields = [field for field in domains_fields if field in domains_df]

            domains_df = domains_df[existing_domains_fields]
            domains_df.rename(columns={
                'company': '公司名称',
                'domain': '根域名',
                'icp': '备案号',
                'toplv_domain': '顶级域名',
                'url': '子域名',
            }, inplace=True)
            domains_df = domains_df.apply(lambda col: col.apply(remove_illegal_characters))
            domains_df.to_excel(writer, sheet_name='域名', index=False)

            adjust_column_widths(writer, '域名')


def emails_data_converter(data: dict, writer):
    if 'data' in data:
        if data['data']:
            emails_df = pd.DataFrame(data['data'])
            emails_fields = [
                'email', 'email_source', 'email_type', 'group', 'mail_domain', 'leakage_account', 'leakage_time',
                'leakage_num'
            ]
            existing_emails_fields = [field for field in emails_fields if field in emails_df.columns]
            emails_df = emails_df[existing_emails_fields]

            emails_df.rename(columns={
                'email': '邮箱',
                'email_source': '邮箱来源',
                'email_type': '邮箱类型',
                'group': '所属公司',
                'mail_domain': '邮箱后缀',
                'leakage_account': '邮箱泄漏信息',
                'leakage_time': '邮箱泄漏时间',
                'leakage_num': '邮箱泄露次数'
            }, inplace=True)
            emails_df = emails_df.apply(lambda col: col.apply(remove_illegal_characters))
            emails_df.to_excel(writer, sheet_name='邮箱', index=False)

            adjust_column_widths(writer, '邮箱')


def codes_data_converter(data: dict, writer):
    if 'data' in data:
        if data['data']:
            codes_df = pd.DataFrame(data['data'])
            codes_fields = [
                'name', 'path', 'url', 'sha', 'keyword', 'tags', 'file_extension'
            ]
            existing_codes_fields = [field for field in codes_fields if field in codes_df]
            codes_df = codes_df[existing_codes_fields]
            codes_df.rename(columns={
                'name': '代码和文档名称',
                'path': '代码路径',
                'url': '代码和文档原文URL',
                'sha': '原文SHA',
                'keyword': '获取关键词',
                'tags': '标签',
                'file_extension': '文件后缀',
                'source': '来源',
                'code_detail': '代码源文',
                'score': '风险值',
                'timestamp_update': '更新时间',
            }, inplace=True)

            owner_list = []
            for item in data['data']:
                owner_info = item.get('owner', {})
                if owner_info:
                    owner_list.append(owner_info)

            owner_df = pd.DataFrame(owner_list)
            owner_fields = [
                'id', 'login', 'url', 'avatar_url'
            ]
            existing_owner_fields = [field for field in owner_fields if field in owner_df]
            owner_df = owner_df[existing_owner_fields]
            owner_df.rename(columns={
                'id': '作者ID',
                'login': '作者用户名/登录号',
                'url': '作者主页',
                'avatar_url': '作者头像'
            }, inplace=True)

            repository_list = []
            for item in data['data']:
                repository_info = item.get('repository', {})
                if repository_info:
                    repository_list.append(repository_info)

            repository_df = pd.DataFrame(repository_list)
            repository_fields = [
                'id', 'name', 'description', 'private', 'url'
            ]
            existing_repository_fields = [field for field in repository_fields if field in repository_df]
            repository_df = repository_df[existing_repository_fields]
            repository_df.rename(columns={
                'id': '仓库id',
                'name': '仓库名称',
                'description': '仓库描述',
                'private': '是否公开',
                'url': '仓库地址'
            }, inplace=True)

            detail_parsing_list = []
            for item in data['data']:
                detail_parsing_info = item.get('detail_parsing', {})
                if detail_parsing_info:
                    detail_parsing_list.append(detail_parsing_info)

            detail_parsing_df = pd.DataFrame(detail_parsing_list)
            detail_parsing_df.rename(columns={
                'domain_list': '原文内的域名列表',
                'email_list': '原文内的邮箱列表',
                'ip_list': '原文内的IP列表',
                'telegram_list': '原文内的telegram账号列表',
                'wangpan_list': '原文内的网盘列表',
            }, inplace=True)

            combined_df = pd.concat([codes_df, owner_df, detail_parsing_df], axis=1)
            combined_df = combined_df.apply(lambda col: col.apply(remove_illegal_characters))
            combined_df.to_excel(writer, sheet_name="代码or文档", index=False)

            adjust_column_widths(writer, "代码or文档")


def personnels_data_converter(data: dict, writer):
    if 'data' in data:
        if data['data']:
            personnels_df = pd.DataFrame(data['data'])
            personnels_fields = [
                'group', 'name'
            ]
            existing_personnels_fields = [field for field in personnels_fields if field in personnels_df]
            personnels_df = personnels_df[existing_personnels_fields]
            personnels_df.rename(columns={
                'group': '公司',
                'name': '姓名',
            }, inplace=True)

            msg_list = []
            for item in data['data']:
                msg_info = item.get('msg', {})
                if msg_info:
                    msg_list.append(msg_info)
            msg_df = pd.DataFrame(msg_list)
            msg_fields = [
                'position', 'introduction'
            ]
            existing_msg_fields = [field for field in msg_fields if field in msg_df]
            msg_df = msg_df[existing_msg_fields]
            msg_df.rename(columns={
                'position': '职位',
                'introduction': '简介'
            }, inplace=True)
            combined_df = pd.concat([personnels_df, msg_df], axis=1)
            combined_df = combined_df.apply(lambda col: col.apply(remove_illegal_characters))
            combined_df.to_excel(writer, sheet_name="人员", index=False)

            adjust_column_widths(writer, "人员")
