#coding=utf-8
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from myauth.decorators import superuser_required

from .models import User, Group
from common.utils import iso8601_to_time
import logging
# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)


#直接使用检查是否管理员
#from django.contrib.auth.decorators import user_passes_test
#@user_passes_test(lambda u: u.is_superuser)

@login_required
@superuser_required
def user(request):
    """        
    所有用户的数据,用于bootstrap-table
    """

    #得到偏移量
    pageIndex= int(request.GET.get('page',1))
    #得到查询个数
    pageSize = int(request.GET.get('limit',10))

    #搜索字段
    searchKey = request.GET.get('searchKey','')
    searchValue = request.GET.get('searchValue','')

    #得到排序字段
    sort = request.GET.get('sort','id')
    #得到排序规则
    order_by_type = request.GET.get('order','asc')
    
    if order_by_type == 'asc':
        order_by = sort
    else:
        order_by = '-' + sort

    data = {}
    data['code'] = 0
    data['msg'] = ""
    data['data'] = []

    if searchKey == '' or searchValue == '':
        #获取所有记录
        data['count'] = User.objects.all().count()
        if pageIndex == 1:
            ormdata = User.objects.all().order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = User.objects.all().order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]
    else:
        if searchKey == 'name':
            data['count'] = User.objects.filter(Q(name__icontains=searchValue)|Q(nickname__icontains=searchValue)|Q(email__icontains=searchValue)).count()
            if pageIndex == 1:
                ormdata = User.objects.filter(Q(name__icontains=searchValue)|Q(nickname__icontains=searchValue)|Q(email__icontains=searchValue)).order_by(order_by)[:pageSize] #offset:limit
            else:
                ormdata = User.objects.filter(Q(name__icontains=searchValue)|Q(nickname__icontains=searchValue)|Q(email__icontains=searchValue)).order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]
        elif searchKey == 'mobile':
            data['count'] = User.objects.filter(mobile__icontains=searchValue).count()
            if pageIndex == 1:
                ormdata = User.objects.filter(mobile__icontains=searchValue).order_by(order_by)[:pageSize] #offset:limit
            else:
                ormdata = User.objects.filter(mobile__icontains=searchValue).order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]
        else:
            return JsonResponse(data)
 
    #获取所有记录
    #data['count'] = User.objects.all().count()
    #if pageIndex == 1:
        #ormdata = User.objects.all().order_by(order_by)[:pageSize] #offset:limit
    #else:
        #ormdata = User.objects.all().order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize] 

    for i in ormdata:
        
        last_login = i.last_login
        if last_login != None:
            last_login = iso8601_to_time(last_login)

        data['data'].append({"id":i.id,
                         "name":i.name,
                         "nickname":i.nickname,
                         "email":i.email,
                         "last_login":last_login,
                         "is_superuser":i.is_superuser,
                         "mobile":i.mobile,
                         "is_active":i.is_active
                         })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)

@login_required
@superuser_required
def group(request):
    """        
    所有用户的数据,用于bootstrap-table
    """

    #得到偏移量
    pageIndex= int(request.GET.get('offset',0))
    #得到查询个数
    pageSize = int(request.GET.get('limit',10))
    #增加状态后解决清空，搜索的limit为搜索的值
    if pageSize < 10:
        pageSize = 10

    #得到排序字段
    sort = request.GET.get('sort','id')
    #得到排序规则
    order_by_type = request.GET.get('order','asc')
    
    if order_by_type == 'asc':
        order_by = sort
    else:
        order_by = '-' + sort

    data = {}
    data['rows'] = []

    #获取所有记录
    data['total'] = Group.objects.all().count()
    #判断起始查询如果是ALL,表示显示全部
    if pageSize != -1:
        ormdata = Group.objects.all().order_by(order_by)[pageIndex:pageIndex + pageSize]
    else:
        ormdata = Group.objects.all().order_by(order_by)
 
    #组ID为key，用户登录名和用户姓名为value
    group_users = {}
    #获取所有用户数据
    user_ormdata = User.objects.filter(is_active=1).filter(is_superuser=0)
    for u in user_ormdata:
        groups = []
        #得到该用户所在的组
        for g in u.groups.all():
            if g.id not in group_users:
                group_users[g.id] = []
            
            group_users[g.id].append("%s(%s)" % (u.name,u.nickname))
        #groups.append(i.id for i in u.groups.all()])

    for i in ormdata:
        
        if i.id in group_users:
            data['rows'].append({"id":i.id,
                                 "name":i.name,
                                 "users":",".join(group_users[i.id])
                                })
        else:
            data['rows'].append({"id":i.id,
                                 "name":i.name,
                                 "users":""
                                })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)

@login_required
@superuser_required
def permissiongroup(request):
    """        
    所有用户的数据,用于bootstrap-table
    """

    #得到偏移量
    pageIndex= int(request.GET.get('offset',0))
    #得到查询个数
    pageSize = int(request.GET.get('limit',10))
    #增加状态后解决清空，搜索的limit为搜索的值
    if pageSize < 10:
        pageSize = 10

    #得到排序字段
    sort = request.GET.get('sort','id')
    #得到排序规则
    order_by_type = request.GET.get('order','asc')
    
    if order_by_type == 'asc':
        order_by = sort
    else:
        order_by = '-' + sort

    data = {}
    data['rows'] = []
    data['total'] = 0
    #获取所有记录
    data['total'] = Group.objects.all().count()
    #判断起始查询如果是ALL,表示显示全部
    if pageSize != -1:
        ormdata = Group.objects.all().order_by(order_by)[pageIndex:pageIndex + pageSize]
    else:
        ormdata = Group.objects.all().order_by(order_by)
 
    for i in ormdata:
        #得到组对应的所有菜单权限,返回一个list
        #menu_ids = i.get_permissions()
        menu_names = i.get_permissions_name()
        data['rows'].append({"id":i.id,
                            "name":i.name,
                            "menus":menu_names
                        })
        
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)

@login_required
@superuser_required
def permissionuser(request):
    """        
    所有用户的数据,用于bootstrap-table
    """

    #得到偏移量
    pageIndex= int(request.GET.get('offset',0))
    #得到查询个数
    pageSize = int(request.GET.get('limit',10))
    #增加状态后解决清空，搜索的limit为搜索的值
    if pageSize < 10:
        pageSize = 10

    #得到排序字段
    sort = request.GET.get('sort','id')
    #得到排序规则
    order_by_type = request.GET.get('order','asc')
    
    if order_by_type == 'asc':
        order_by = sort
    else:
        order_by = '-' + sort

    data = {}
    data['rows'] = []

    #获取所有记录
    data['total'] = User.objects.filter(is_active=1).filter(is_superuser=0).count()
    #判断起始查询如果是ALL,表示显示全部
    if pageSize != -1:
        ormdata = User.objects.filter(is_active=1).filter(is_superuser=0).order_by(order_by)[pageIndex:pageIndex + pageSize]
    else:
        ormdata = User.objects.filter(is_active=1).filter(is_superuser=0).order_by(order_by)
 
    for i in ormdata:
        #得到组对应的所有菜单权限,返回一个list
        #menu_ids = i.get_permissions()
        menu_names = i.get_permissions_name(i)
        data['rows'].append({"id":i.id,
                            "name":i.name,
                            "menus":menu_names
                        })

    return JsonResponse(data)


@login_required
@superuser_required
def setValue(request):
    """        
    修改用户状态和管理员状态
    """

    _id = request.GET.get('id')
    value = request.GET.get('value')
    tag = request.GET.get('tag')
    
    if request.user.id == int(_id):
        data = {'code':0,'msg':'禁止操作自身'}
        return JsonResponse(data)
        
    if tag == 'status':
        #修改状态
        User.objects.filter(id=_id).update(is_active=value)
        data = {'code':1,'msg':'操作成功'}
    elif tag == 'super':
        #修改是否管理员
        User.objects.filter(id=_id).update(is_superuser=value)
        data = {'code':1,'msg':'操作成功'}
    else:
        data = {'code':0,'msg':'未知操作'}

    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)