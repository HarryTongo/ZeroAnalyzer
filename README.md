ZeroAnalyzer/            # 零零信安数据收集处理  
├── README.md  
├── requirements.txt     # 依赖  
├── main.py              # 主入口文件，调用不同的 API 接口并处理数据  
├── config.py            # 配置文件  
├── data_to_excel.py     # 处理json数据转换为excl  
├── api/                 # 存放 API 相关模块  
│   ├── __init__.py  
│   ├── info_system.py   # 信息系统相关接口  
│   ├── mobile_apps.py   # 移动端应用相关接口  
│   ├── domains.py       # 域名相关接口  
│   ├── emails.py        # 邮箱相关接口  
│   ├── code_docs.py     # 代码文档相关接口  
│   └── personnels.py    # 人员信息相关接口  
├── data/                # 存放原始 JSON 数据  
│   └── __init__.py #   
└── result/              # 存放处理后的数据Excel  
