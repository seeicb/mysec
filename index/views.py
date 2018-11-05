from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from index.models import Target, Subdomain, Ipinfo

# Create your views here.

# 测试用
def root(request):
    return render(request,'root.html')


def index(request):
    return render(request,'target_list.html')


def test(request):
    return render(request,'test.html')


# 增加目标页面
def target_add(request):
    return render(request,'target_add.html')


# 目标详情页
def target(request, target_id):
    obj = Target.objects.get(id=target_id)
    ipcount = Subdomain.objects.filter(target_id=target_id).values('ip').distinct().count()
    subdomain_count = Subdomain.objects.filter(target_id=target_id).count()
    return render(request, 'target.html', {'obj': obj, 'ipcount': ipcount, 'subdomain_count': subdomain_count})


def target_edit(request,target_id):
    obj = Target.objects.get(id=target_id)
    return render(request,'target_edit.html',{'obj':obj})



def subdomain_list(request,target_id):
    return render(request,'subdomain_list.html',{'target_id':target_id})


def ip_list(request,target_id):
    return render(request,'ip_list.html',{'target_id':target_id})


