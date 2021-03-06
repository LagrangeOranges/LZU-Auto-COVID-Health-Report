#!/usr/bin/env python
# -*-coding:utf-8-*-
# by 'hollowman6' from Lanzhou University(兰州大学)

import os
import sys
import requests
import json
import urllib.parse

sckey = os.environ['SERVERCHANSCKEY']
openid = os.environ['OPENID']
pptoken = os.environ['PPTOKEN']
pptopic = os.environ['PPTOPIC']
status = sys.argv[1]
info = ""
errorServerChan = ""

if sckey:
    try:
        with open("information.txt") as infofile:
            info = urllib.parse.quote_plus(
                infofile.read().replace('\n', '\n\n'))
    except Exception as e:
        print(e)
    finally:
        if not info:
            info = "工作流或者打卡程序存在问题，请查看运行记录并提交issue!"
            status = "failure"
        message = "%E5%A4%B1%E8%B4%A5%E2%9C%96"
        if status == "success":
            message = "%E6%88%90%E5%8A%9F%E2%9C%94"
        host = "https://sc.ftqq.com/"
        user = ""
        if openid:
            host = "https://sctapi.ftqq.com/"
            if openid != "0":
                user = "&openid=" + openid
        res = requests.get(host + sckey + ".send?text=" + message +
                           "%E5%85%B0%E5%B7%9E%E5%A4%A7%E5%AD%A6%E8%87%AA%E5%8A%A8%E5%81%A5%E5%BA%B7%E6%89%93%E5%8D%A1&desp=" + info + user)
        result = json.loads(res.text)
        if not openid and result['errno'] == 0:
            print("成功通过Sever酱将结果通知给用户!")
        elif openid and result['data']['errno'] == 0:
            if openid == "0":
                print("成功通过Sever酱将结果通知到测试公众号的创建用户!")
            else:
                print("成功通过Sever酱将结果通知到测试公众号的指定关注用户和创建用户!")
        else:
            errorServerChan = "Server酱推送错误: " + res.text
else:
    print("未设置SERVERCHANSCKEY，尝试使用PushPlus...")

if pptoken:
    try:
        with open("information.txt") as infofile:
            info = urllib.parse.quote_plus(
                infofile.read().replace('***************************\n', "", 1).replace(
                    "***************************\n", "<hr>").replace('\n', '<br>'))
    except Exception as e:
        print(e)
    finally:
        if not info:
            info = "工作流或者打卡程序存在问题，请查看运行记录并提交issue!"
            status = "failure"
        message = "%E5%A4%B1%E8%B4%A5%E2%9C%96"
        if status == "success":
            message = "%E6%88%90%E5%8A%9F%E2%9C%94"
        host = "http://pushplus.hxtrip.com/"
        user = ""
        res = requests.get(host + "send?token=" + pptoken + "&title=" + message +
                           "%E5%85%B0%E5%B7%9E%E5%A4%A7%E5%AD%A6%E8%87%AA%E5%8A%A8%E5%81%A5%E5%BA%B7%E6%89%93%E5%8D%A1&content=" + info
                           + "&template=html&topic=" + pptopic)
        result = json.loads(res.text)
        if result['code'] == 200:
            print("成功通过PushPlus将结果通知给相关用户!")
        else:
            raise Exception("PushPlus推送错误: " + res.text +
                            "\n" + errorServerChan)
else:
    print("未设置PPTOKEN！")

if errorServerChan:
    raise Exception(errorServerChan)
