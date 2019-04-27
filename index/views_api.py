import json
import datetime
from django.http import HttpResponse
from index.models import Target, Subdomain, Ipinfo,CTarget,CIpDomain
from index import task


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)


def convert_to_dicts(objs):
    obj_arr = []
    for o in objs:
        dict = {}
        dict.update(o.__dict__)
        dict.pop("model", None)
        dict.pop("_state", None)
        dict.pop("pk", None)
        obj_arr.append(dict)
    return obj_arr


def api_target_add(request):
    target_name = request.POST['target_name']
    main_host = request.POST['main_host']
    remark = request.POST['remark']
    target = Target(target_name=target_name, remark=remark, main_host=main_host)
    target.save()
    resp = {'code': 1, 'msg': '增加成功', 'data': {}}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def api_target_edit(request):
    obj = Target.objects.get(id=request.POST['target_id'])
    obj.target_name = request.POST['target_name']
    obj.remark = request.POST['remark']
    obj.main_host = request.POST['main_host']
    obj.save()
    resp = {'code': 1, 'msg': '编辑成功', 'data': {}}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def api_target_del(request):
    target_id = request.POST['target_id']
    Target.objects.filter(id=target_id).delete()
    Subdomain.objects.filter(target_id=target_id).delete()
    resp = {'code': 1, 'msg': '删除成功', 'data': {}}
    return HttpResponse(json.dumps(resp), content_type="application/json")



def api_target_list(request):
    objs = Target.objects.all()
    dict_data = convert_to_dicts(objs)
    json_data = {'code': 0, 'msg': '', 'count': 100, 'data': dict_data}
    data = json.dumps(json_data, cls=CJsonEncoder)
    return HttpResponse(data, content_type="application/json")


def api_domain_list(request, target_id):
    objs = Subdomain.objects.filter(target_id=target_id)
    dict_data = convert_to_dicts(objs)
    json_data = {'code': 0, 'msg': '', 'count': 100, 'data': dict_data}
    data = json.dumps(json_data, cls=CJsonEncoder)
    return HttpResponse(data, content_type="application/json")


def api_ip_list(request, target_id):
    objs = Ipinfo.objects.filter(target_id=target_id)
    dict_data = convert_to_dicts(objs)
    json_data = {'code': 0, 'msg': '', 'count': 100, 'data': dict_data}
    data = json.dumps(json_data, cls=CJsonEncoder)
    return HttpResponse(data, content_type="application/json")


def api_target_scan(request):
    target_id = request.POST['target_id']
    task.startscan.delay(target_id)
    resp = {'code': 1, 'msg': '开始扫描', 'data': {}}
    return HttpResponse(json.dumps(resp), content_type="application/json")

# ---------------- C段API接口 -------------------------------

def api_c_add(request):
    target_name = request.POST['target_name']
    c_ip = request.POST['c_ip']
    remark = request.POST['remark']
    target = CTarget(target_name=target_name, remark=remark, c_ip=c_ip)
    target.save()
    resp = {'code': 1, 'msg': '增加成功', 'data': {}}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def api_c_list(request):
    objs = CTarget.objects.all()
    dict_data = convert_to_dicts(objs)
    json_data = {'code': 0, 'msg': '', 'count': 100, 'data': dict_data}
    data = json.dumps(json_data, cls=CJsonEncoder)
    return HttpResponse(data, content_type="application/json")


def api_c_scan(request):
    target_id = request.POST['target_id']
    task.start_bingc_scan.delay(target_id)
    resp = {'code': 1, 'msg': '开始扫描', 'data': {}}
    return HttpResponse(json.dumps(resp), content_type="application/json")

def api_c_ip2doamin_list(request, target_id):

    objs = CIpDomain.objects.filter(target_id=target_id)
    dict_data = convert_to_dicts(objs)
    json_data = {'code': 0, 'msg': '', 'count': 100, 'data': dict_data}
    data = json.dumps(json_data, cls=CJsonEncoder)
    return HttpResponse(data, content_type="application/json")