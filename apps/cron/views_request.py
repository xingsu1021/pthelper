#coding=utf-8
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import datetime
from .models import JobType, Job, Log


#直接使用检查是否管理员
#from django.contrib.auth.decorators import user_passes_test
#@user_passes_test(lambda u: u.is_superuser)

@login_required
def jobtype(request):
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

        data['count'] = JobType.objects.count()
        if pageIndex == 1:
            ormdata = JobType.objects.order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = JobType.objects.order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]
    else:

        data['count'] = JobType.objects.filter(Q(name__icontains=searchValue)).count()
        if pageIndex == 1:
            ormdata = JobType.objects.filter(Q(name__icontains=searchValue)).order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = JobType.objects.filter(Q(name__icontains=searchValue)).order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]

    for i in ormdata:
        
        data['data'].append({"id":i.id,
                         "name":i.name,
                         "type_id":i.type_id,
                         })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)

#------------------------------------------
@login_required
def job(request):
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

        data['count'] = Job.objects.count()
        if pageIndex == 1:
            ormdata = Job.objects.order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = Job.objects.order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]
    else:

        data['count'] = Job.objects.filter(Q(name__icontains=searchValue)).count()
        if pageIndex == 1:
            ormdata = Job.objects.filter(Q(name__icontains=searchValue)).order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = Job.objects.filter(Q(name__icontains=searchValue)).order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]

    for i in ormdata:
            
        data['data'].append({"id":i.id,
                         "name":i.name,
                         "jobtype_id":i.jobtype_id,
                         "crontab_time":i.crontab_time,
                         "crontab_status":i.crontab_status,
                         })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)


#------------------------------------------
@login_required
def log(request):
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

        data['count'] = Log.objects.count()
        if pageIndex == 1:
            ormdata = Log.objects.order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = Log.objects.order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]
    else:

        data['count'] = Log.objects.filter(Q(name__icontains=searchValue)).count()
        if pageIndex == 1:
            ormdata = Log.objects.filter(Q(name__icontains=searchValue)).order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = Log.objects.filter(Q(name__icontains=searchValue)).order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]

    for i in ormdata:
            
        data['data'].append({"id":i.id,
                         "name":i.name,
                         "type_id":i.type_id,
                         "crontab_id":i.crontab_id,
                         "site_name":i.site_name,
                         "message":i.message,
                         "created_at":i.created_at,
                         "status":i.status,
                         })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)


#==================
@login_required
def jobtypeinfo(request):
    """ 
    任务类型
    xmSelect
    """

    data = {}
    data['code'] = 0
    data['msg'] = ""
    data['data'] = []

    #得到排序字段
    sort = request.GET.get('sort','type_id')
    #得到排序规则
    order_by_type = request.GET.get('order','')
    
    if order_by_type == 'asc':
        order_by = sort
    else:
        order_by = '-' + sort

    #获取所有记录
    data['count'] = JobType.objects.count()

    ormdata = JobType.objects.order_by(order_by).all()

    for i in ormdata:

        data['data'].append({
                         "name":i.name,
                         "type_id":i.type_id
                         })
   

    return JsonResponse(data)

@login_required
def jobtimetype(request):
    """ 
    任务类型
    xmSelect
    """

    data = {}
    data['code'] = 0
    data['msg'] = ""
    data['data'] = []

    cron_time_data = [
            {"name": '每小时', "value": "hour"},
            {"name": '每天', "value": "day"},
            {"name": 'N分钟', "value": "minute_n"}

            ]
    #获取所有记录
    data['count'] = 7

    for i in cron_time_data:

        data['data'].append({
                         "name":i['name'],
                         "value":i['value']
                         })
   

    return JsonResponse(data)

@login_required
def loginfo(request):
    """ 
    任务日志
    
    """

    data = {}
    data['code'] = 0
    data['msg'] = ""
    data['data'] = []

    #GET用于签到任务日志展示
    if request.method == "GET":
        #获取任务id
        crontab_id = request.GET.get('crontab_id')
        #得到排序字段
        sort = request.GET.get('sort','created_at')
        #得到排序规则
        order_by_type = request.GET.get('order','')
        
        if order_by_type == 'asc':
            order_by = sort
        else:
            order_by = '-' + sort
    
        if crontab_id == "" or crontab_id == None:
            response_data={"code":0,"msg":"无任务记录"}
    
            return JsonResponse(response_data)
        
        #获取今天日期
        today = datetime.datetime.today()
        #获取所有记录
        data['count'] = Log.objects.filter(crontab_id=crontab_id).filter(created_at__date=today).count()
    
        ormdata = Log.objects.filter(crontab_id=crontab_id).filter(created_at__date=today).order_by(order_by)
    
        for i in ormdata:
            
            data['data'].append({'id':i.id,
                             "name":i.name,
                             "type_id":i.type_id,
                             "message":i.message
                             })            
    
        return JsonResponse(data)
    
    #POST用于首页展示识别列表
    if request.method == "POST":

        order_by = 'created_at'
        #获取今天日期
        today = datetime.datetime.today()
        #获取今天签到失败记录
        data['count'] = Log.objects.filter(type_id=1000).filter(status=False).filter(created_at__date=today).count()
        
        ormdata = Log.objects.filter(type_id=1000).filter(status=False).filter(created_at__date=today).order_by(order_by)
        
        for i in ormdata:
            
            data['data'].append({'id':i.id,
                             "name":i.site_name,
                             "message":i.message
                             })            
    
        return JsonResponse(data)        

    
