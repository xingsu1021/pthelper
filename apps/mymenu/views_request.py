#coding=utf-8
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from myauth.decorators import superuser_required

from .models import Menu
from myauth.models import Group,User

@login_required
@superuser_required
def menu(request):
    """        
    所有的数据,用于bootstrap-table
    """

    #得到偏移量
    pageIndex= int(request.GET.get('offset',0))
    #得到查询个数
    pageSize = int(request.GET.get('limit',10))
    #增加状态后解决清空，搜索的limit为搜索的值
    if pageSize < 10:
        pageSize = 10

    #得到搜索字段
    search_key = request.GET.get('search')
    #得到搜索类型，html中自定义
    search_type = request.GET.get('search_type')

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

    if search_key=="" or search_key == None:
        #获取所有记录
        data['total'] = Menu.objects.all().count()
        #判断起始查询如果是ALL,表示显示全部
        if pageSize != -1:
            ormdata = Menu.objects.all().order_by(order_by)[pageIndex:pageIndex + pageSize]
        else:
            ormdata = Menu.objects.all().order_by(order_by)
    else:
        #拼接搜索
        key = "name like '%%" +search_key +"%%'"
        
        #获取所有记录        
        data['total'] = Menu.objects.filter(Q(name__contains=search_key)).count()
        #判断起始查询如果是ALL,表示显示全部
        if pageSize != -1:
            ormdata = Menu.objects.filter(Q(name__contains=search_key)).order_by(order_by)[pageIndex:pageSize]
        else:
            ormdata = Menu.objects.filter(Q(name__contains=search_key)).order_by(order_by)   

    for i in ormdata:
        #如果没有上级菜单，就是顶级，如果存在上级菜单，获取上级菜单的中文名称
        if i.menupid == 0:
            menupid = "顶级"
        else:
            get_menu_ormdata = Menu.objects.get(id=i.menupid)
            menupid = get_menu_ormdata.name
            
        if i.menutype == 1:
            menutype = "菜单"
        else:
            menutype = "功能"

        data['rows'].append({"id": i.id,
                             "name": i.name,
                             "menuurl": i.menuurl,
                             "menupid":menupid,
                             "menuseq": i.menuseq,
                             "menutype": menutype
                             })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)

@login_required
@superuser_required
def menuztree(request):
    """
    用于ztree 菜单树
    """

    data = []

    #得到所有菜单
    ormdata = Menu.objects.all().order_by('menuseq')

    for i in ormdata:
        data.append({"name":i.name,
                        "id":i.id,
                        "pId":i.menupid,
                        "open":True
                        })        

    return JsonResponse(data, safe=False)

@login_required
@superuser_required
def groupmenuztree(request):
    """
    用于ztree 用户组菜单权限树
    """
    #接收组权限ID
    _id = request.GET.get("id")
    data = []

    #得到所有菜单
    ormdata = Menu.objects.all()
    #组
    group = Group.objects.get(id=_id)

    for i in ormdata:
        #得到组所在的菜单id list
        menu_ids = group.get_permissions()
        if i.id in menu_ids:
            data.append({"name":i.name,
                            "id":i.id,
                            "pId":i.menupid,
                            "checked":True,
                            "open":True
                            }) 
        else:
            data.append({"name":i.name,
                            "id":i.id,
                            "pId":i.menupid
                            })        

    return JsonResponse(data, safe=False)

@login_required
@superuser_required
def usermenuztree(request):
    """
    用于ztree 用户菜单权限树
    """
    #接收组权限ID
    _id = request.GET.get("id")
    data = []

    #得到所有菜单
    ormdata = Menu.objects.all()
    #用户
    user = User.objects.get(id=_id)

    for i in ormdata:
        #得到组所在的菜单id list
        menu_ids = user.get_permissions(user)
        if i.id in menu_ids:
            data.append({"name":i.name,
                            "id":i.id,
                            "pId":i.menupid,
                            "checked":True,
                            "open":True
                            }) 
        else:
            data.append({"name":i.name,
                            "id":i.id,
                            "pId":i.menupid
                            })        

    return JsonResponse(data, safe=False)