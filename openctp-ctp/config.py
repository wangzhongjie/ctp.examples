# @Project: https://github.com/Jedore/ctp.examples
# @File:    base.py
# @Time:    03/06/2024 21:38
# @Author:  Jedore
# @Email:   jedorefight@gmail.com
# @Addr:    https://github.com/Jedore

# 配置了 SimNow 常用的四个环境
# 可以使用监控平台 http://openctp.cn 查看前置服务是否正常
# 也可以按需配置其他的支持 ctp官方ctpapi库的柜台
# 注意需要同时修改相应的 user/password/broker_id/authcode/appid 等信息
# 账户需要到 SimNow 官网申请 https://www.simnow.com.cn/

# SimNow 提供的四个环境

import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

username1 = os.getenv('username1')
password1 = os.getenv('password1')

username2 = os.getenv('username2')
password2 = os.getenv('password2')
authcode2 = os.getenv('authcode2')
# print(username2,password2,authcode2)

envs = {
    "7x24": {
        "td": "tcp://180.168.146.187:10130",
        "md": "tcp://180.168.146.187:10131",
        "user_id": username1,
        "password": password1,
        "broker_id": "9999",
        "authcode": "0000000000000000",
        "appid": "simnow_client_test",
        "user_product_info": "",
    },
    "电信1": {
        "td": "tcp://180.168.146.187:10201",
        "md": "tcp://180.168.146.187:10211",
        "user_id": username1,
        "password": password1,
        "broker_id": "9999",
        "authcode": "0000000000000000",
        "appid": "simnow_client_test",
        "user_product_info": "",
    },
    "电信2": {
        "td": "tcp://180.168.146.187:10202",
        "md": "tcp://180.168.146.187:10212",
        "user_id": username1,
        "password": password1,
        "broker_id": "9999",
        "authcode": "0000000000000000",
        "appid": "simnow_client_test",
        "user_product_info": "",
    },
    "移动": {
        "td": "tcp://218.202.237.33:10203",
        "md": "tcp://218.202.237.33:10213",
        "user_id": username1,
        "password": password1,
        "broker_id": "9999",
        "authcode": "0000000000000000",
        "appid": "simnow_client_test",
        "user_product_info": "",
    },



    "gtja电信1": {
        "td": "tcp://114.94.128.1:42205", # 交易前置地址
        "md": "tcp://114.94.128.1:42213", # 行情前置地址
        "user_id": username2,
        "password": password2,
        "broker_id": "2071",
        "authcode": authcode2,
        "appid": "client_Dimension6_1.0",
        "user_product_info": "Dimension6",
        "product_info": "client_Dimension6_1",
    },
    "gtja电信2": {
        "td": "tcp://114.94.128.5:42205", # 交易前置地址
        "md": "tcp://114.94.128.5:42213", # 行情前置地址
        "user_id": username2,
        "password": password2,
        "broker_id": "2071",
        "authcode": authcode2,
        "appid": "client_Dimension6_1.0",
        "user_product_info": "Dimension6",
        "product_info": "client_Dimension6_1",
    },
    "gtja电信3": {
        "td": "tcp://114.94.128.6:42205", # 交易前置地址
        "md": "tcp://114.94.128.6:42213", # 行情前置地址
        "user_id": username2,
        "password": password2,
        "broker_id": "2071",
        "authcode": authcode2,
        "appid": "client_Dimension6_1.0",
        "user_product_info": "Dimension6",
        "product_info": "client_Dimension6_1",
    },
    "gtja联通1": {
        "td": "tcp://140.206.34.161:42205", # 交易前置地址
        "md": "tcp://140.206.34.161:42213", # 行情前置地址
        "user_id": username2,
        "password": password2,
        "broker_id": "2071",
        "authcode": authcode2,
        "appid": "client_Dimension6_1.0",
        "user_product_info": "Dimension6",
        "product_info": "client_Dimension6_1",
    },
    "gtja联通2": {
        "td": "tcp://140.206.34.165:42205", # 交易前置地址
        "md": "tcp://140.206.34.165:42213", # 行情前置地址
        "user_id": username2,
        "password": password2,
        "broker_id": "2071",
        "authcode": authcode2,
        "appid": "client_Dimension6_1.0",
        "user_product_info": "Dimension6",
        "product_info": "client_Dimension6_1",
    },
    "gtja联通3": {
        "td": "tcp://140.206.34.166:42205", # 交易前置地址
        "md": "tcp://140.206.34.166:42213", # 行情前置地址
        "user_id": username2,
        "password": password2,
        "broker_id": "2071",
        "authcode": authcode2,
        "appid": "client_Dimension6_1.0",
        "user_product_info": "Dimension6",
        "product_info": "client_Dimension6_1",
    },
    "gtja内网1": {
        "td": "tcp://10.74.33.160:42205", # 交易前置地址
        "md": "tcp://10.74.33.160:42213", # 行情前置地址
        "user_id": username2,
        "password": password2,
        "broker_id": "2071",
        "authcode": authcode2,
        "appid": "client_Dimension6_1.0",
        "user_product_info": "Dimension6",
        "product_info": "client_Dimension6_1",
    },
    "gtja内网2": {
        "td": "tcp://10.74.33.161:42205", # 交易前置地址
        "md": "tcp://10.74.33.161:42213", # 行情前置地址
        "user_id": username2,
        "password": password2,
        "broker_id": "2071",
        "authcode": authcode2,
        "appid": "client_Dimension6_1.0",
        "user_product_info": "Dimension6",
        "product_info": "client_Dimension6_1",
    },
    "gtja内网3": {
        "td": "tcp://10.74.33.162:42205", # 交易前置地址
        "md": "tcp://10.74.33.162:42213", # 行情前置地址
        "user_id": username2,
        "password": password2,
        "broker_id": "2071",
        "authcode": authcode2,
        "appid": "client_Dimension6_1.0",
        "user_product_info": "Dimension6",
        "product_info": "client_Dimension6_1",
    },

}
