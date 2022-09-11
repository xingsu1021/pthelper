#coding=utf-8
from django.http import JsonResponse, StreamingHttpResponse,HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from transmission_rpc import Client
import qbittorrentapi

from .models import Tools
from common.utils import parseUrl

#直接使用检查是否管理员
#from django.contrib.auth.decorators import user_passes_test
#@user_passes_test(lambda u: u.is_superuser)

@login_required
def tools(request):
    """        
    提供相应的数据
    """

    #得到偏移量
    pageIndex= int(request.GET.get('page',1))
    #得到查询个数
    pageSize = int(request.GET.get('limit',10))

    #搜索字段
    searchKey = request.GET.get('searchKey','')
    searchValue = request.GET.get('searchValue','')
    #去掉空格
    searchValue = searchValue.strip()

    #得到排序字段
    sort = request.GET.get('sort','id')
    #得到排序规则
    order_by_type = request.GET.get('order','')
    
    if order_by_type == 'asc':
        order_by = sort
    else:
        order_by = '-' + sort

    data = {}
    data['code'] = 0
    data['msg'] = ""
    data['data'] = []

    if searchValue == '':

        data['count'] = Tools.objects.count()
        if pageIndex == 1:
            ormdata = Tools.objects.order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = Tools.objects.order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]
    else:

        data['count'] = Tools.objects.filter(Q(name__icontains=searchValue)|Q(typed__icontains=searchValue)).count()
        if pageIndex == 1:
            ormdata = Tools.objects.filter(Q(name__icontains=searchValue)|Q(typed__icontains=searchValue)).order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = Tools.objects.filter(Q(name__icontains=searchValue)|Q(typed__icontains=searchValue)).order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]

    for i in ormdata:
        
        data['data'].append({"id":i.id,
                         "name":i.name,
                         "typed":i.typed,
                         "username":i.username,
                         "url":i.url,
                         "password":i.password,
                         "dirname":i.dirname,
                         })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)

#==================
@login_required
def tools_test(request):
    """
    测试下载器配置连通性
    """
    
    url = request.POST.get("url").strip()
    typed = request.POST.get("typed").strip()
    username = request.POST.get("username").strip()
    password = request.POST.get("password").strip()
    
    url_data = parseUrl(url)
    
    if typed == 'tr':
        try:
            
            c = Client(protocol= url_data['protocol'],
                   host=url_data['host'], 
                   port=url_data['port'], 
                   username=username, 
                   password=password, 
                   timeout = 10
                   )
            
            response_data={"code":1,"msg": "连接成功" }
        except:
            response_data={"code":0,"msg": "连接失败" }
    elif typed == 'qb':
        
        c = qbittorrentapi.Client(
            host=url_data['host'],
            port=url_data['port'],
            username=username,
            password=password,
        )
        
        try:
            c.auth_log_in()
            response_data={"code":1,"msg": "连接成功" }
        except:
            response_data={"code":0,"msg": "连接失败" } 
        
    return JsonResponse(response_data)

#==================
@login_required
def select_tools(request):
    """ 
    RSS规则
    xmSelect
    """

    data = {}
    data['code'] = 0
    data['msg'] = ""
    data['data'] = []

    
    #得到排序字段
    sort = request.GET.get('sort','id')
    #得到排序规则
    order_by_type = request.GET.get('order','')
    
    if order_by_type == 'asc':
        order_by = sort
    else:
        order_by = '-' + sort
        
    #获取所有记录
    data['count'] = Tools.objects.count()

    ormdata = Tools.objects.order_by(order_by).all()
 

    for i in ormdata:

        data['data'].append({
                         "id":i.id,
                         "name":i.name
                         })

    return JsonResponse(data)