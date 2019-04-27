from __future__ import absolute_import, unicode_literals
from celery import shared_task
import nmap
from index.util.scan import domian_scan
from index.util.bingc import bingc
from index.models import Subdomain, Target, Ipinfo,CTarget,CIpDomain

# from celery.signals import worker_process_init
# from multiprocessing import current_process
#
# @worker_process_init.connect
# def fix_multiprocessing(**kwargs):
#     try:
#         current_process()._config
#     except AttributeError:
#         current_process()._config = {'semprefix': '/mp'}


@shared_task
def startscan(target_id):
    target_obj = Target.objects.get(id=target_id)
    print(target_obj.main_host)
    target_obj.status = 1
    target_obj.save()
    domain_list = (target_obj.main_host.split(';'))
    for domain in domain_list:
        print('开始扫描域名：' + domain)
        a, b, c = domian_scan(domain)

        for i in range(len(a)):
            obj = Subdomain(target_id=target_id, first_domain=domain, sub_domain=a[i], ip=b[i], ip_addr=c[i])
            obj.save()

    ipobj = Subdomain.objects.filter(target_id=target_id).values('ip').distinct()

    for i in ipobj:
        host = i['ip']

        if not host:
            continue
        print("start scan:" + host)
        nm = nmap.PortScanner()
        nm.scan(host,arguments='-sS -T4 -Pn --top-ports 1000',sudo=True)
        if nm[host].state()!='up':
            print(host+':down')
            obj = Ipinfo(target_id=target_id, ip=host, host_state='down', port=0, protocol="-", port_state="-",
                         name="-", version="-")
            obj.save()
            continue

        try:
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                lport = sorted(lport)
                for port in lport:
                    portocols = proto
                    port_state = nm[host][proto][port]['state']
                    name = nm[host][proto][port]['name']
                    product = nm[host][proto][port]['product']
                    temp_version = nm[host][proto][port]['version']
                    extrainfo = nm[host][proto][port]['extrainfo']
                    version = product + "-" + temp_version + "-" + extrainfo
                    print(product+'--'+version)
                    obj = Ipinfo(target_id=target_id, ip=i['ip'], host_state='up', port=port, protocol=portocols,
                                 port_state=port_state, name=name, version=version)
                    obj.save()
        except:
            print(host + ":scna error")
            obj = Ipinfo(target_id=target_id, ip=host, host_state='error', port=0, protocol="-", port_state="-",
                         name="-", version="-")

            obj.save()
    # scan done
    target_obj.status = 2
    target_obj.save()


@shared_task
def start_bingc_scan(target_id):

    target_obj = CTarget.objects.get(id=target_id)
    print(target_obj.c_ip)
    target_obj.status = 1
    target_obj.save()
    c_result=bingc(target_obj.c_ip)

    for i in c_result:
        x=i.split(":",1)
        print(x)
        obj=CIpDomain(target_id=target_id,ip=x[0],domain=x[1],remark="")
        obj.save()
    target_obj.status = 2
    target_obj.save()

    print("扫描完成，域名数量: " + str(len(c_result)))


