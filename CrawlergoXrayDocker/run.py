#! coding=utf-8

import time
import subprocess
from multiprocessing import Process

crawlergo_path = '/root/crawlergo_linux_amd64'
xray_path = '/root/xray_linux_amd64'
report_output = f'/root/output_{int(time.time())}.html'

def crawlergo(target):
    '''
    调用爬虫
    '''
    try:
        # /root/crawlergo_linux_amd64 -c chromium-browser -t 20 -f smart --fuzz-path --robots-path --push-to-proxy http://127.0.0.1:7777 testphp.vulnweb.com
        crawlergo_res = subprocess.run([f'{crawlergo_path} -c chromium-browser -t 20 -f smart --fuzz-path --push-to-proxy http://127.0.0.1:7777 {target}'], shell=True)
        print(crawlergo_res)
    except Exception as e:
        print(e)


def xray_listen():
    '''
    xray 被动扫描
    '''
    try:
        # /root/xray_linux_amd64 webscan --listen 127.0.0.1:7777 --html-output vul-temp.html
        xray_res = subprocess.run([f'{xray_path} webscan --listen 127.0.0.1:7777 --html-output {report_output}'], shell=True)
        print(xray_res)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    file = open('targets.txt', 'r')
    print('[+] targets.txt load ok')
    p = Process(target=xray_listen)
    p.start()

    for target in file.readlines():
            url = ''.join(target.split('\n'))
            try:
                print(f'[+] now scan : {url}')
                crawlergo(url)
            except Exception as e:
                print(e)
                continue
    
    print(f'[+] xray report output {report_output}')
    print('[+] crawlergo end.')