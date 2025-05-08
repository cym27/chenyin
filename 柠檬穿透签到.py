import requests
import os
import time

def loginandcheckin(account, password):
    # 创建会话
    session = requests.Session()

    # 登录URL
    loginurl = "https://gost.sian.one/api/v1/auth/login"
    # 签到URL
    checkinurl = "https://gost.sian.one/api/v1/auth/checkin"
    # 用户信息URL
    userinfourl = "https://gost.sian.one/api/v1/auth/userInfo"

    # 登录请求头部
    loginheaders = {
        "Host": "gost.sian.one",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "\"Windows\"",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://gost.sian.one",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://gost.sian.one/",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Priority": "u=1, i"
    }

    # 登录请求数据
    logindata = {
        "account": account,
        "password": password
    }

    try:
        # 发送登录请求
        loginresponse = session.post(loginurl, headers=loginheaders, json=logindata)
        loginresponse.raise_for_status()  # 检查请求是否成功
        responsedata = loginresponse.json()

        if responsedata.get("code") == 0:
            print(f"登录成功 >>>>> 账号: {account}")
            token = responsedata["data"]["token"]

            # 签到请求头部
            checkinheaders = {
                "Host": "gost.sian.one",
                "Connection": "keep-alive",
                "sec-ch-ua-platform": "\"Windows\"",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Origin": "https://gost.sian.one",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://gost.sian.one/",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Priority": "u=1, i",
                "Token": token
            }

            # 发送签到请求
            checkin_response = session.post(checkinurl, headers=checkinheaders)
            checkin_response.raise_for_status()  # 检查请求是否成功
            checkindata = checkin_response.json()
            print(checkindata)  # 直接打印签到返回的数据

            # 用户信息请求头部
            userinfoheaders = {
                "Host": "gost.sian.one",
                "Connection": "keep-alive",
                "sec-ch-ua-platform": "\"Windows\"",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Origin": "https://gost.sian.one",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://gost.sian.one/",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Priority": "u=1, i",
                "Token": token
            }

            # 发送用户信息请求
            userinforesponse = session.post(userinfourl, headers=userinfoheaders)
            userinforesponse.raise_for_status()  # 检查请求是否成功
            userinfodata = userinforesponse.json()

            if userinfodata.get("code") == 0:
                # 打印amount的值
                amount = userinfodata["data"]["amount"]
                print(f"积分: {amount}")
            else:
                print("获取用户信息失败，code不是0")
        else:
            print("登录失败 >>>>> 账号:", account)
            print("错误信息:", responsedata.get('message', '未知错误'))
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")

def main():
    # 检测环境变量
    TOKEN = os.getenv("gostauth")
    if not TOKEN:
        print("未检测到环境变量 gostauth，请设置环境变量或使用内置变量")
        return

    account_list = TOKEN.split("&")
    print(f">>>> 共检测到 {len(account_list)} 个账号，开始运行Gost登录")

    for index, account_info in enumerate(account_list):
        print(f"-------- 第 {index + 1} 个账号 --------")
        if ":" in account_info:
            account, password = account_info.split(":", 1)
            loginandcheckin(account, password)  # 修正函数名
            time.sleep(2)  # 避免请求过于频繁
        else:
            print(f"账号格式错误: {account_info} (应为 account:password 格式)")

if __name__ == "__main__":
    main()