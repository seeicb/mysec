# coding:utf-8

"""
Usage:
  python bingC.py IP/MASK [output_path]
Example:
  python bingC.py 132.12.43.0/24 result.txt
  python bingC.py 132.12.43.0/24
"""

# import urllib
# import urllib2
# import base64
import requests
import queue
import threading
import re
import sys
import time
import IPy
import json



# config配置
top = 50
skip = 0
# 修改为你的主账户密钥
accountKey = 'JaDRZblJ6OheyvTxxxxxxxxxxxxxxxxWx8OThobZoRA'
# 修改此项为True，开启API搜索
ENABLE_API = False

queue = queue.Queue()
ips=set()

result=[]
lock = threading.Lock()
thread_num = 20
# thread.daemon = True





#
# def BingSearch(query):
#     payload = {}
#     payload['$top'] = top
#     payload['$skip'] = skip
#     payload['$format'] = 'json'
#     payload['Query'] = "'" + query + "'"
#     url = 'https://api.datamarket.azure.com/Bing/Search/Web?' + urllib.urlencode(payload)
#     sAuth = 'Basic ' + base64.b64encode(':' + accountKey)
#
#     headers = {}
#     headers['Authorization'] = sAuth
#     try:
#         req = urllib2.Request(url, headers=headers)
#         response = urllib2.urlopen(req)
#         the_page = response.read()
#         data = json.loads(the_page)
#         return data
#     except Exception as e:
#         print(e)





def scan():
    global thread_num
    while 1:
        if queue.qsize() > 0:
            ip = queue.get()
            if ENABLE_API:
                print("关闭API接口")
                # print("[*]api enabled!")
                # ans_obj = BingSearch("ip:" + ip)
                # for each in ans_obj['d']['results']:
                #     ips.add(ip + ' -> ' + each['Url'].split('://')[-1].split('/')[0] + " | " + each['Title'])
            else:
                # print("查找IP"+ip)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
                }

                q = "https://www.bing.com/search?q=ip:" + ip
                c = requests.get(q, headers=headers)
                p = re.compile(r'<cite>(.*?)</cite>')
                c=c.content.decode('GBK','ignore')
                l = re.findall(p, c)
                for each in l:
                    domain = each.split('://')[-1].split('/')[0]
                    if domain=="ip.chinaz.com":
                        continue
                    msg = ip + ':' + domain
                    # print("结果"+msg)
                    ips.add(msg)



        else:
            thread_num -= 1
            break


# def api_scan():
#     global thread_num
#     while 1:
#         if queue.qsize() > 0:
#             BingSearch(queue.get())
#



def runThreads():
    print("Running...")
    for i in range(thread_num):
        t = threading.Thread(target=scan, name=str(i))
        t.setDaemon(True)
        t.start()
    # It can quit with Ctrl-C
    while 1:
        if thread_num > 0:
            time.sleep(0.01)
        else:
            break


def bingc(cip):

    print("C段查找"+cip)

    try:
        _list = IPy.IP(cip)
    except Exception as e:
        sys.exit('Invalid IP/MASK, %s' % e)
    for each in _list:
        queue.put(str(each))

    runThreads()


    # print(ips)

    return ips

