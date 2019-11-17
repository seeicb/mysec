import requests
import json
import os


def domian_scan(domain):
    subdomain = []
    iplist = []
    geoiplist = []
    outfile = 'index/util/result/' + domain + '.txt'
    cmd = "index/util/amass enum -brute  -ip -o %s -d %s" % (outfile, domain)
    os.system(cmd)
    with open(outfile, 'r') as f:
        for line in f.readlines():
            tmp = line.strip().split()
            subdomain.append(tmp[0])
            iplist.append(tmp[1])
            geoiplist.append(get_geoip(tmp[1]))
    return subdomain,iplist,geoiplist


# 根据IP获取地理位置
def get_geoip(ip):
    url = "http://api.ip138.com/query/?ip=%s&token=3957f4fd056cd1767bc5aeed4efa4c76" % ip
    r = requests.get(url)
    html_respon = json.loads(r.text)
    geoip = ''.join(html_respon['data'])
    return geoip
