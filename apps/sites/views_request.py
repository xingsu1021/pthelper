#coding=utf-8
from django.http import JsonResponse, StreamingHttpResponse,HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import simplejson as json
import io
from urllib import parse
import tempfile
import datetime

from common.sites_user import userIngress
from .models import SiteConfig, SiteRank, SiteInfo, SiteUser
from rss.models import Config

#直接使用检查是否管理员
#from django.contrib.auth.decorators import user_passes_test
#@user_passes_test(lambda u: u.is_superuser)

@login_required
def siteconfig(request):
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

        data['count'] = SiteConfig.objects.count()
        if pageIndex == 1:
            ormdata = SiteConfig.objects.order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = SiteConfig.objects.order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]
    else:

        data['count'] = SiteConfig.objects.filter(Q(name__icontains=searchValue)|Q(name_cn__icontains=searchValue)).count()
        if pageIndex == 1:
            ormdata = SiteConfig.objects.filter(Q(name__icontains=searchValue)|Q(name_cn__icontains=searchValue)).order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = SiteConfig.objects.filter(Q(name__icontains=searchValue)|Q(name_cn__icontains=searchValue)).order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]

    for i in ormdata:
        
        data['data'].append({"id":i.id,
                         "name":i.name,
                         "name_cn":i.name_cn,
                         "index_url":i.index_url,
                         "sign_type":i.sign_type,
                         })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)

@login_required
def siterankconfig(request):
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

        data['count'] = SiteRank.objects.count()
        if pageIndex == 1:
            ormdata = SiteRank.objects.order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = SiteRank.objects.order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]
    else:

        data['count'] = SiteRank.objects.filter(Q(name__icontains=searchValue)|Q(siteconfig_name__icontains=searchValue)).count()
        if pageIndex == 1:
            ormdata = SiteRank.objects.filter(Q(name__icontains=searchValue)|Q(siteconfig_name__icontains=searchValue)).order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = SiteRank.objects.filter(Q(name__icontains=searchValue)|Q(siteconfig_name__icontains=searchValue)).order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]

    for i in ormdata:
        
        data['data'].append({"id":i.id,
                         "name":i.name,
                         "siteconfig_name":i.siteconfig_name,
                         "download":i.download,
                         "up_time":i.up_time,
                         "upload":i.upload,
                         "ratio":i.ratio,
                         "privilege":i.privilege,
                         "serial_number":i.serial_number,
                         })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)


#===================================================================================================
@login_required
def siteinfo(request):
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

        data['count'] = SiteInfo.objects.count()
        if pageIndex == 1:
            ormdata = SiteInfo.objects.order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = SiteInfo.objects.order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]
    else:

        data['count'] = SiteInfo.objects.filter(Q(siteconfig_name__icontains=searchValue)|Q(siteconfig_name_cn__icontains=searchValue)).count()
        if pageIndex == 1:
            ormdata = SiteInfo.objects.filter(Q(siteconfig_name__icontains=searchValue)|Q(siteconfig_name_cn__icontains=searchValue)).order_by(order_by)[:pageSize] #offset:limit
        else:
            ormdata = SiteInfo.objects.filter(Q(siteconfig_name__icontains=searchValue)|Q(siteconfig_name_cn__icontains=searchValue)).order_by(order_by)[pageSize*(pageIndex-1):pageIndex * pageSize]

    for i in ormdata:
        
        #siteconfig_ormdata = SiteConfig.objects.get(name=i.siteconfig_name)
        
        data['data'].append({"id":i.id,
                         "siteconfig_name":i.siteconfig_name,
                         'siteconfig_name_cn':i.siteconfig_name_cn,
                         "cookie":i.cookie,
                         "passkey":i.passkey,
                         })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)

#===================================================================================================
@login_required
def siteuser(request):
    """        
    提供相应的数据
    """
    
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

    data['count'] = SiteConfig.objects.count()
    ormdata = SiteUser.objects.order_by(order_by)

    #已经配置的站点列表
    siteconfig_names = list(SiteInfo.objects.all().values_list('siteconfig_name',flat=True))
    
    for i in ormdata:
        ormdata_siteconfig = SiteConfig.objects.get(name=i.siteinfo_id.siteconfig_name)
        data['data'].append({"id":i.id,
                             "site_name":i.siteinfo_id.siteconfig_name + '(' + i.siteinfo_id.siteconfig_name_cn + ')',
                             "site_url": ormdata_siteconfig.index_url,
                             'username':i.username,
                             "uid":i.uid,
                             "ratio":i.ratio,
                             "upload":i.upload,
                             "download":i.download,
                             "bonus":i.bonus,
                             "score":i.score,
                             "level":i.level,
                             "published_seed_num":i.published_seed_num,
                             "seed_num":i.seed_num,
                             "totle_seed_size":i.totle_seed_size,
                             "create_time":i.create_time,
                             "invite":i.invite,
                             })
        #删除已经获取数据的
        siteconfig_names.remove(i.siteinfo_id.siteconfig_name)
        
    for i in siteconfig_names:
        ormdata_siteconfig = SiteConfig.objects.get(name=i)
        data['data'].append({"site_name":ormdata_siteconfig.name + '(' + ormdata_siteconfig.name_cn + ')',
                             "site_url": ormdata_siteconfig.index_url,
                             'username':"无数据",
                             })
    #返回json串
    #return HttpResponse(json.dumps(data,ensure_ascii = False), "application/json")
    return JsonResponse(data)

#=====================================================================================================================
def get_stream(data):
    # 开始这里我用ByteIO流总是出错，但是后来参考廖雪峰网站用StringIO就没问题
    file = io.StringIO()
    data=json.dumps(data)
    file.write(data)
    res=file.getvalue()
    file.close()
    return res

#==================
@login_required
def siteconfigExport(request):
    """        
    文件导出
    """

    ids = []
    #fetch方法
    if request.method == "PUT":
        body = request.body
        json_body = json.loads(body) 

        ids = json_body['ids']
        
    data = []

    if len(ids) == 0:
        ormdata = SiteConfig.objects.all()
    else:
        ormdata = SiteConfig.objects.filter(id__in=ids)

    for i in ormdata:
        
        data.append({"name":i.name,
                    "name_cn":i.name_cn,
                    "index_url":i.index_url,
                    "torrent_url":i.torrent_url,
                    "bonus_url":i.bonus_url,
                    "sign_type":i.sign_type,
                    })
    #print(data)
    json_stream=get_stream(data)
    response = HttpResponse(content_type='application/json')
    
    response['Content-Disposition'] = 'attachment;filename=' + parse.quote('pthelper站点配置') + '.json'
    response.write(json_stream)

    return response

#==================
@login_required
def siteconfigImport(request):
    """        
    文件上传
    """
    data = {}
    data['code'] = 0
    data['msg'] = ""
    data['data'] = []

    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        #data = get_stream(file_obj)
        
        file_temp = tempfile.NamedTemporaryFile()
        file_temp.write(file_obj.read())
        #res=file_temp.getvalue()
        file_temp.seek(0)
        data = file_temp.read()
        file_temp.close()
        
        #print(data)
        try:
            json_data = json.loads(data)
            for i in json_data:
                name = i['name']
                name_cn = i['name_cn']
                index_url = i['index_url']
                torrent_url = i['torrent_url']
                bonus_url = i['bonus_url']
                sign_type = i['sign_type']
                
                get_site = SiteConfig.objects.filter(name=name).count()
                if get_site == 0:
                    SiteConfig.objects.create(name = name,
                                              name_cn = name_cn,
                                              index_url = index_url,
                                              torrent_url = torrent_url,
                                              bonus_url = bonus_url,
                                              sign_type = sign_type
                                              )
                else:
                    #更新站点配置
                    SiteConfig.objects.filter(name=name).update(name_cn = name_cn,
                                                                index_url = index_url,
                                                                torrent_url = torrent_url,
                                                                bonus_url = bonus_url,
                                                                sign_type = sign_type
                                                                )
            response_data={"code":1,"msg":"更新成功"}
            
        except:
            response_data={"code":0,"msg":"非法文件"}

    return JsonResponse(response_data)

#==================
@login_required
def siteinfoExport(request):
    """        
    文件导出
    """

    #得到批量或者单个要删除的id
    #ids = request.POST.getlist("ids[]")
    #print("ids====>",ids)
    ids = []
    #fetch方法
    if request.method == "PUT":
        body = request.body
        json_body = json.loads(body) 

        ids = json_body['ids']
        
    data = []

    if len(ids) == 0:
        ormdata = SiteInfo.objects.all()
    else:
        ormdata = SiteInfo.objects.filter(id__in=ids)

    for i in ormdata:
        
        data.append({"name":i.siteconfig_name,
                     "name_cn":i.siteconfig_name_cn,
                    "cookie":i.cookie,
                    "passkey":i.passkey,
                    })
    #print(data)
    json_stream=get_stream(data)
    response = HttpResponse(content_type='application/json')
    
    response['Content-Disposition'] = 'attachment;filename=' + parse.quote('pthelper站点信息') + '.json'
    response.write(json_stream)

    return response

#==================
@login_required
def siteinfoImport(request):
    """        
    文件上传
    """
    data = {}
    data['code'] = 0
    data['msg'] = ""
    data['data'] = []

    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        #data = get_stream(file_obj)
        
        file_temp = tempfile.NamedTemporaryFile()
        file_temp.write(file_obj.read())
        #res=file_temp.getvalue()
        file_temp.seek(0)
        data = file_temp.read()
        file_temp.close()
        
        #print(data)
        try:
            json_data = json.loads(data)
            for i in json_data:
                siteconfig_name = i['name']
                cookie = i['cookie']
                passkey = i['passkey']
                siteconfig_name_cn = i['name_cn']
                
                get_site = SiteInfo.objects.filter(siteconfig_name=siteconfig_name).count()
                if get_site == 0:
                    SiteInfo.objects.create(siteconfig_name = siteconfig_name,
                                            cookie = cookie,
                                            passkey = passkey,
                                            siteconfig_name_cn = siteconfig_name_cn
                                            )
                else:
                    #更新站点配置
                    SiteInfo.objects.filter(siteconfig_name=siteconfig_name).update(cookie = cookie,
                                                                        passkey=passkey,
                                                                        siteconfig_name_cn=siteconfig_name_cn
                                                                        )
            response_data={"code":1,"msg":"更新成功"}
            
        except:
            response_data={"code":0,"msg":"非法文件"}

    return JsonResponse(response_data)


#==================
@login_required
def siteconfigname(request):
    """ 
    网站集合
    xmSelect
    """

    data = {}
    data['code'] = 0
    data['msg'] = ""
    data['data'] = []

    #获取数据标志 1 返回所有 其它返回未配置站点
    flag = request.GET.get('flag', 0)
    
    #得到排序字段
    sort = request.GET.get('sort','name')
    #得到排序规则
    order_by_type = request.GET.get('order','')
    
    if order_by_type == 'asc':
        order_by = sort
    else:
        order_by = '-' + sort
        
    #获取所有记录
    data['count'] = SiteConfig.objects.count()

    ormdata = SiteConfig.objects.order_by(order_by).all()
    
    if int(flag) == 0:
        #获取siteinfo中配置的站点名
        ormdata_siteinfo = list(SiteInfo.objects.values_list('siteconfig_name', flat=True))
    else:
        ormdata_siteinfo = []

    for i in ormdata:
        #忽略已经配置的站点
        if i.name not in ormdata_siteinfo:
            data['data'].append({
                             "name":i.name,
                             "name_en_cn":i.name + "(" + i.name_cn + ")"
                             })

    return JsonResponse(data)


#==================
@login_required
def select_siteinfo(request):
    """ 
    RSS订阅
    xmSelect
    """

    data = {}
    data['code'] = 0
    data['msg'] = ""
    data['data'] = []

    #获取数据标志 1 返回所有 其它返回未配置站点
    flag = request.GET.get('flag', 0)
    
    #得到排序字段
    sort = request.GET.get('sort','id')
    #得到排序规则
    order_by_type = request.GET.get('order','')
    
    if order_by_type == 'asc':
        order_by = sort
    else:
        order_by = '-' + sort
        
    #获取所有记录
    data['count'] = SiteInfo.objects.count()

    ormdata = SiteInfo.objects.order_by(order_by).all()
 
    if int(flag) == 0:
        #获取RSS配置的站点ID
        ormdata_config = list(Config.objects.values_list('siteinfo_id', flat=True))
    else:
        ormdata_config = []

    for i in ormdata:
        #只返回未配置rss的站点
        if i.id not in ormdata_config:
            data['data'].append({
                             "id":i.id,
                             "name":i.siteconfig_name + "(" + i.siteconfig_name_cn + ")"
                             })

    return JsonResponse(data)


#===============================================================================
def getUserInfo(request):
    """
    更新用户信息
    """

    #保存最后发送的结果
    send_data = []
    count_siteinfo = SiteInfo.objects.count()
    #未配置任何站点直接返回
    if count_siteinfo == 0:
        return
        
    _TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    ormdata_siteinfo = SiteInfo.objects.all()
    for i in ormdata_siteinfo:
        #记录ID值
        site_id = i.id
        site_name = i.siteconfig_name
        site_cookie = i.cookie
        site_name_cn = i.siteconfig_name_cn
        #获取站点配置信息
        site_config = SiteConfig.objects.get(name=site_name)
        site_url = site_config.index_url
        site_sign_type = site_config.sign_type
        
        flag, data = userIngress(site_name, site_name_cn, site_url, site_cookie, site_sign_type)
        if flag:
            count_userinfo = SiteUser.objects.filter(siteinfo_id = site_id).count()
            if count_userinfo == 0:
                #无记录
                SiteUser.objects.create(siteinfo_id=i,
                                        username = data['user_name'],
                                        uid = int(data['user_id']),
                                        invite = int(data['invite']),
                                        create_time = datetime.datetime.strptime(data['create_time'].strip(), _TIME_FORMAT).strftime('%Y-%m-%d %H:%M:%S'),
                                        ratio = data['ratio'].strip(),
                                        upload = data['upload'].strip(),
                                        download = data['download'].strip(),
                                        bonus = data['bonus'],
                                        score = data['score'],
                                        level = data['level'],
                                        published_seed_num = int(data['published_seed_num']),
                                        seed_num = int(data['seed_num']),
                                        totle_seed_size = data['totle_seed_size']
                                        )
            else:
                #已经存在
                SiteUser.objects.filter(siteinfo_id=site_id).update(username = data['user_name'],
                                                                    uid = int(data['user_id']),
                                                                    invite = int(data['invite']),
                                                                    ratio = data['ratio'].strip(),
                                                                    upload = data['upload'].strip(),
                                                                    download = data['download'].strip(),
                                                                    bonus = data['bonus'],
                                                                    score = data['score'],
                                                                    level = data['level'],
                                                                    published_seed_num = int(data['published_seed_num']),
                                                                    seed_num = int(data['seed_num']),
                                                                    totle_seed_size = data['totle_seed_size']
                                                                    )
    
    response_data={"code":1,"msg":"更新成功"}

    return JsonResponse(response_data)