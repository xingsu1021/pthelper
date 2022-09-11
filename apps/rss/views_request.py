#coding=utf-8
from django.http import JsonResponse, StreamingHttpResponse,HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from transmission_rpc import Client
import qbittorrentapi

from .models import Config, Rule, SeedInfo
from cron.crontabs import my_scheduler
from common.utils import filesizeformat, parseUrl

#直接使用检查是否管理员
#from django.contrib.auth.decorators import user_passes_test
#@user_passes_test(lambda u: u.is_superuser)

@login_required
def config(request):
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

        data['count'] = Config.objects.count()
        if pageIndex == 1:
            ormdata = Config.objects.order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = Config.objects.order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]
    else:

        data['count'] = Config.objects.filter(Q(name__icontains=searchValue)|Q(name_cn__icontains=searchValue)).count()
        if pageIndex == 1:
            ormdata = Config.objects.filter(Q(name__icontains=searchValue)|Q(name_cn__icontains=searchValue)).order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = Config.objects.filter(Q(name__icontains=searchValue)|Q(name_cn__icontains=searchValue)).order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]

    for i in ormdata:
        
        data['data'].append({"id":i.id,
                         "site_name":i.siteinfo_id.siteconfig_name + '(' + i.siteinfo_id.siteconfig_name_cn + ')',
                         "url":i.url,
                         })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)

#===================================================================================================================
@login_required
def rule(request):
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

        data['count'] = Rule.objects.count()
        if pageIndex == 1:
            ormdata = Rule.objects.order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = Rule.objects.order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]
    else:

        data['count'] = Rule.objects.filter(Q(name__icontains=searchValue)).count()
        if pageIndex == 1:
            ormdata = Rule.objects.filter(Q(name__icontains=searchValue)).order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = Rule.objects.filter(Q(name__icontains=searchValue)).order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]

    for i in ormdata:
        
        data['data'].append({"id":i.id,
                         #"config_id":i.config_id.siteinfo_id.siteconfig_name_cn,
                         "config_id":i.config_id.siteinfo_id.siteconfig_name + '(' + i.config_id.siteinfo_id.siteconfig_name_cn + ')',
                         "tools_id":i.tools_id.name,
                         "name":i.name,
                         "keyword":i.keyword,
                         "status":i.status,
                         "refresh_time":i.refresh_time,
                         "rate":i.rate,
                         "is_paused":i.is_paused
                         })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)

#===================================================================================================================
@login_required
def seedinfo(request):
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

        data['count'] = SeedInfo.objects.count()
        if pageIndex == 1:
            ormdata = SeedInfo.objects.order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = SeedInfo.objects.order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]
    else:

        data['count'] = SeedInfo.objects.filter(Q(seed_name__icontains=searchValue)).count()
        if pageIndex == 1:
            ormdata = SeedInfo.objects.filter(Q(seed_name__icontains=searchValue)).order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = SeedInfo.objects.filter(Q(seed_name__icontains=searchValue)).order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]

    for i in ormdata:
        
        data['data'].append({"id":i.id,
                         "siteinfo_id":i.siteinfo_id.siteconfig_name + '(' + i.siteinfo_id.siteconfig_name_cn + ')',                         
                         "seed_name":i.seed_name,
                         "seed_type":i.seed_type,
                         "seed_published_time":i.seed_published_time,
                         "seed_file_size":filesizeformat(i.seed_file_size),
                         "seed_status":i.seed_status,
                         "seed_details_link":i.seed_details_link,
                         })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)
#===================================================================================================================
@login_required
def checkbox_setRuleStatus(request):
    """        
    设置规则启用，禁用
    """

    _id = request.GET.get('id')
    value = request.GET.get('value')
    tag = request.GET.get('tag')
    
    ormdata_rule = Rule.objects.get(id=_id)

    if tag == 'status':
        #修改状态
        Rule.objects.filter(id=_id).update(status=int(value))
        if int(value) == 1:
            #激活任务
            minute = '*/%s' % ormdata_rule.refresh_time
            my_scheduler(crontab_id = ormdata_rule.job_id.crontab_id, crontab_status = True, minute=minute,  jobtype_id=1002 )
        else:
            #禁用任务
            my_scheduler(crontab_id = ormdata_rule.job_id.crontab_id, action="del" )

        data = {'code':1,'msg':'操作成功'}
    else:
        data = {'code':0,'msg':'未知操作'}

    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)

#==================
@login_required
def select_rssconfig(request):
    """ 
    RSS订阅
    xmSelect
    """

    data = {}
    data['code'] = 0
    data['msg'] = ""
    data['data'] = []

    #获取数据标志 1 返回所有 其它返回未配置站点
    #flag = request.GET.get('flag', 0)
    
    #得到排序字段
    sort = request.GET.get('sort','id')
    #得到排序规则
    order_by_type = request.GET.get('order','')
    
    if order_by_type == 'asc':
        order_by = sort
    else:
        order_by = '-' + sort
        
    #获取所有记录
    data['count'] = Config.objects.count()

    ormdata = Config.objects.order_by(order_by).all()

    for i in ormdata:
        data['data'].append({
                             "id":i.id,
                             "name":i.siteinfo_id.siteconfig_name + "(" + i.siteinfo_id.siteconfig_name_cn + ")"
                             })

    return JsonResponse(data)

            
#==================
@login_required
def seed_download(request):
    """
    下载种子
    """
    #种子ID
    seed_id = request.POST.get("id")
    
    ormdata_seedinfo = SeedInfo.objects.get(id = seed_id)
    #下载连接
    seed_donwload_link = ormdata_seedinfo.seed_donwload_link
    #下载器类型
    download_type = ormdata_seedinfo.rule_id.tools_id.typed
    download_username = ormdata_seedinfo.rule_id.tools_id.username
    download_password = ormdata_seedinfo.rule_id.tools_id.password
    download_url = ormdata_seedinfo.rule_id.tools_id.url
    #下载目录
    download_dirname = ormdata_seedinfo.rule_id.tools_id.dirname
    
    if download_dirname == "":
        download_dirname = None
        
    url_data = parseUrl(download_url)
    
    if download_type == 'tr':
        try:
            
            c = Client(protocol= url_data['protocol'],
                   host=url_data['host'], 
                   port=url_data['port'], 
                   username=download_username, 
                   password=download_password, 
                   timeout = 10
                   )
            
            torrent = c.add_torrent(seed_donwload_link,
                          timeout = 10,
                          download_dir = download_dirname
                          
                          )
            #获取种子id
            torrent_id = torrent.id
            
            ormdata_seedinfo.seed_torrent_id = torrent_id
            ormdata_seedinfo.seed_status = True
            ormdata_seedinfo.save()
            
            response_data={"code":1,"msg": "添加成功" }
        except Exception as e:
            print(e)
            response_data={"code":0,"msg": "添加失败" }
    elif download_type == 'qb':
        
        c = qbittorrentapi.Client(
            host=url_data['host'],
            port=url_data['port'],
            username=download_username,
            password=download_password,
        )
        
        try:
            c.auth_log_in()
            response_data={"code":1,"msg": "添加成功" }
        except:
            response_data={"code":0,"msg": "添加失败" } 
        
    return JsonResponse(response_data)