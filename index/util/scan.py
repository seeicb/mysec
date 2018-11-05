from .subDomainsBrute import subDomainBrute
from .sublist3r import sublist3r
import socket
import requests
import re

def domian_scan(domain):
    list1 = subDomainBrute(domain)
    list2=sublist3r(domain)

    subdomain_list = list(set(list1 + list2))
    print('域名合并结果：',subdomain_list)
    iplist,geoiplist=get_ip(subdomain_list)
    return  subdomain_list,iplist,geoiplist


# 根据域名获取ip
def get_ip(domainlist):
    iplist = []
    geoiplist = []
    for i in range(len(domainlist)):
        try:
            ipaddr = socket.gethostbyname(domainlist[i])
            geoip = get_geoip(ipaddr)
        except:
            ipaddr = ""
            geoip = ""
        iplist.append(ipaddr)
        geoiplist.append(geoip)
    # print(iplist,geoiplist)
    return iplist, geoiplist



# 根据IP获取地理位置
def get_geoip(ip):
    url = "http://www.ip138.com/ips1388.asp?ip=%s&action=2" % ip
    r = requests.get(url)
    r.encoding = "gb2312"
    html_respon = r.text
    ma = re.compile("本站数据：(.*?)</li>")
    pa = ma.search(html_respon)
    geoip = pa.group()[5:-5]
    return geoip
