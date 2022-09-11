# coding=utf-8
from django.conf import settings
import requests
import datetime
from urllib import parse
import os
import logging
from bs4 import BeautifulSoup
import feedparser
from thefuzz import process
from transmission_rpc import Client
import qbittorrentapi

from common.utils import send_email,send_telegram,send_iyuu, send_enwechat, parseUrl
from common.sites_sign import signIngress
from sites.models import SiteConfig, SiteInfo
from .models import Job, Log
from notify.models import NotifyConfig
from rss.models import Rule, SeedInfo

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from django_apscheduler.jobstores import DjangoJobStore, register_job

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'

logger = logging.getLogger('sign')

executors = {
    # 执行器的线程与进程数
    'default': ThreadPoolExecutor(10),
    'processpool': ProcessPoolExecutor(10)
}

jobstores = {
    'default': DjangoJobStore()
}

job_defaults = {
    # 最近多久时间内允许存在的任务数
    'misfire_grace_time': 10,
    # 该定时任务允许最大的实例个数
    'max_instances': 2,
    # 是否运行一次最新的任务，当多个任务堆积时
    #'coalesce': True,
    #存在相同任务直接覆盖
    'replace_existing': True,
}

# 1.实例化调度器
scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE,job_defaults=job_defaults)
# 2.调度器使用DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), "default")
# 5.开启定时任务
scheduler.start()
#try:
    ## 3.设置定时任务
    ## 另一种方式为每天固定时间执行任务，对应代码为
    #@register_job(scheduler,"cron", second="*/10",id="test", replace_existing=True)
    #def my_job():
        ## 这里写你要执行的任务
        #format_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        #print(format_time)
    ## 5.开启定时任务
    #scheduler.start()
    #print("Scheduler started!")
#except Exception as e:
    #print(e)
    ## 有错误就停止定时器
    #scheduler.shutdown()
    
def my_scheduler(crontab_id=None, crontab_status=None, hour="*", minute="*", jobtype_id=1000, action='add'):
    """计划任务调度
    crontab_id 任务ID
    crontab_status 任务状态(配置状态非任务本身状态),bool
    jobtype_id 任务类型id
    """
    
    # 创建任务
    #scheduler.add_job(test, 'cron', hour=hour, minute=minute, second=second, args=[s])
    isJob = scheduler.get_job(crontab_id)

    if isJob != None:

        #删除job
        if action=='del':
            scheduler.remove_job(crontab_id)
            return True
            
        #立刻执行任务
        if action == 'now' and jobtype_id == 1000:
            scheduler.add_job(sign, 'interval', trigger='date', next_run_time=datetime.datetime.now(), id=crontab_id)
            return True
            
        #激活
        if crontab_status:
            #已经存在的任务不能做时间修改，必须删除在添加
            scheduler.remove_job(crontab_id)
            if jobtype_id == 1000:
                #签到
                scheduler.add_job(sign, 'cron', hour=hour, minute=minute, id=crontab_id, args=[crontab_id])
            elif jobtype_id == 1003:
                #重签
                scheduler.add_job(re_fail_sign, 'cron', hour=hour, minute=minute, id=crontab_id, args=[crontab_id])
            elif jobtype_id == 1002:
                #RSS订阅
                scheduler.add_job(rss, 'cron', hour=hour, minute=minute, id=crontab_id, args=[crontab_id])            

        else:
            #禁用状态，直接删除任务
            scheduler.remove_job(crontab_id)
            #暂停任务
            #scheduler.pause_job(crontab_id)

    else:
        #无状态任务处理(常规为立刻执行任务)
        #立刻执行签到任务
        if action == 'now' and jobtype_id == 1000:
            #只执行一次
            scheduler.add_job(signonekey, trigger='date', next_run_time=datetime.datetime.now(), id=crontab_id)
            return True 
        
        #启用添加，禁用忽略
        if crontab_status:
            if jobtype_id == 1000:
                scheduler.add_job(sign, 'cron', hour=hour, minute=minute, id=crontab_id, args=[crontab_id])
            elif jobtype_id == 1003:
                scheduler.add_job(re_fail_sign, 'cron', hour=hour, minute=minute, id=crontab_id, args=[crontab_id])
            elif jobtype_id == 1002:
                scheduler.add_job(rss, 'cron', hour=hour, minute=minute, id=crontab_id, args=[crontab_id])            
           
            
    return True
            
    
def sign(crontab_id):
    """
    执行签到
    参数：
      crontab_id：执行任务的ID
    """

    #获取任务ID对应的站点
    job_sites = list(Job.objects.filter(crontab_id=crontab_id).values_list('sites',flat=True))
    
    #保存最后发送的结果
    send_data = []
    site_count = SiteInfo.objects.count()
    if site_count == 0:
        send_data.append('未配置任何站点')
    else:
        if job_sites[0] == None or len(job_sites[0]) == 0:
            #获取所有已经配置的站点
            sites = SiteInfo.objects.all()
        else:
            #将站点字符串塞进list
            job_sites = [x for x in job_sites[0].split(',')]
            sites = SiteInfo.objects.filter(siteconfig_name__in=job_sites)
            
        for i in sites:
            site_name = i.siteconfig_name
            site_cookie = i.cookie
            #获取站点配置信息
            site_config = SiteConfig.objects.get(name=site_name)
            site_url = site_config.index_url
            site_name_cn = site_config.name_cn
            site_sign_type = site_config.sign_type
     
            #headers = {
                #'user-agent': user_agent,
                #'referer': site_url,
                #'cookie': site_cookie
            #}
            #统一签到入口
            flag, data = signIngress(site_name, site_name_cn, site_url, site_cookie, site_sign_type) 
            
            try:
                Log.objects.create(name = '签到',type_id = 1000, crontab_id = crontab_id, site_name=site_name, message = data, status = flag)
            except:
                logger.error("%s(%s)数据返回出错" % (site_name, site_name_cn))
                #防止返回数据错误导致异常退出
                continue

            send_data.append(data)
            
    #发送消息
    send_msg(crontab_id, send_data, title='签到提示')
    
    return


def signonekey():
    """
    一键执行签到
    参数：
      crontab_id：执行任务的ID
    """

    #获取任务ID对应的站点
    job_sites = list(Job.objects.filter(jobtype_id=1000).values_list('sites',flat=True))
    crontab_id = list(Job.objects.filter(jobtype_id=1000).values_list('crontab_id',flat=True))[0]
    
    #保存最后发送的结果
    send_data = []
    site_count = SiteInfo.objects.count()
    if site_count == 0:
        send_data.append('未配置任何站点')
    else:
        if job_sites[0] == None or len(job_sites[0]) == 0:
            #获取所有已经配置的站点
            sites = SiteInfo.objects.all()
        else:
            #将站点字符串塞进list
            job_sites = [x for x in job_sites[0].split(',')]            
            sites = SiteInfo.objects.filter(siteconfig_name__in=job_sites)
            
        for i in sites:
            site_name = i.siteconfig_name
            site_cookie = i.cookie
            #获取站点配置信息
            site_config = SiteConfig.objects.get(name=site_name)
            site_url = site_config.index_url
            site_name_cn = site_config.name_cn
            site_sign_type = site_config.sign_type
     
            #headers = {
                #'user-agent': user_agent,
                #'referer': site_url,
                #'cookie': site_cookie
            #}
            #统一签到入口
            flag, data = signIngress(site_name, site_name_cn, site_url, site_cookie, site_sign_type) 
            
            try:
                Log.objects.create(name = '签到',type_id = 1000, crontab_id = crontab_id, site_name=site_name, message = data, status = flag)
            except:
                logger.error("%s(%s)数据返回出错" % (site_name, site_name_cn))
                #防止返回数据错误导致异常退出
                continue

            send_data.append(data)
            
    #发送消息
    send_msg(crontab_id, send_data, title='签到提示')
    
    return

def re_fail_sign(crontab_id):
    """
    重试签到失败
    """
    
    #保存最后发送的结果
    send_data = []
    
    order_by = 'created_at'
    #获取今天日期
    today = datetime.datetime.today()
    #统计失败记录
    fail_num = Log.objects.filter(type_id=1000).filter(status=False).filter(created_at__date=today).count()
    
    #获取今天签到失败记录
    ormdata = Log.objects.filter(type_id=1000).filter(status=False).filter(created_at__date=today).order_by(order_by)
    
    #无失败记录
    if fail_num == 0:
        return
        
    for i in ormdata:
        #日志记录id
        log_id = i.id
        #站点英文名
        name = i.site_name
        #失败返回消息
        message = i.message
        
        #忽略cookie失效的站点
        if 'cookie' in message:
            continue
        
        #获取配置的站点信息
        site_info = SiteInfo.objects.get(siteconfig_name=name)

        site_name = site_info.siteconfig_name
        site_cookie = site_info.cookie
        #获取站点配置信息
        site_config = SiteConfig.objects.get(name=site_name)
        site_url = site_config.index_url
        site_name_cn = site_config.name_cn
        site_sign_type = site_config.sign_type
     
        #统一签到入口
        flag, data = signIngress(site_name, site_name_cn, site_url, site_cookie, site_sign_type)
                
        #补签成功，刷新状态
        if flag:
            Log.objects.filter(id=log_id).update(status=flag)
            
        send_data.append(data)
    #不为0发送
    if len(send_data) != 0:
        
        #发送消息
        send_msg(crontab_id, send_data, title='补签提示')
    
    return

def send_msg(crontab_id = None, send_data = [], title='PT助手提示'):
    """
    发送消息
    """
    logger.info("-------------send_data-------------------")
    logger.info(",".join(send_data))
    #获取对应任务ID的记录详情
    notify_ormdata = Job.objects.get(crontab_id = crontab_id)
    if 'iyuu' in notify_ormdata.notifys:
        
        iyuu_ormdata = NotifyConfig.objects.get(name='iyuu')
        
        flag,msg = send_iyuu(iyuu_ormdata.iyuu_key, send_data, title = title)
        logger.info("-------------iyuu-------------------")
        logger.info(msg)
        
    if 'telegram' in notify_ormdata.notifys:
        tg_ormdata = NotifyConfig.objects.get(name='telegram')
        flag,msg = send_telegram(tg_ormdata.tg_chat_id,tg_ormdata.tg_token,send_data, title = title)
        logger.info("-------------telegram-------------------")
        logger.info(msg)
        
    if 'email' in notify_ormdata.notifys:
        email_ormdata = NotifyConfig.objects.get(name='email')
        
        receiver_users = [x for x in email_ormdata.receive_user.split(',')]
        flag,msg = send_email(email_ormdata.mail_type,email_ormdata.smtp_user,email_ormdata.smtp_password,receiver_users,send_data, title = title)
        logger.info("-------------email-------------------")
        logger.info(msg)   
        
    if 'enwechat' in notify_ormdata.notifys:
        enwechat_ormdata = NotifyConfig.objects.get(name='enwechat')
        
        receiver_users = [x for x in enwechat_ormdata.receive_user.split(',')]
        flag, msg = send_enwechat(corp_id=enwechat_ormdata.enwechat_corp_id, 
                                 agent_id=enwechat_ormdata.enwechat_agent_id, 
                                 agent_secret=enwechat_ormdata.enwechat_agent_secret,
                                 user_ids = receiver_users,
                                 send_data = send_data,
                                 title = title
                                 )
        
        logger.info("-------------enwechat-------------------")
        logger.info(msg)
        
    return

#==========================================================================================================
def rss(crontab_id):
    """
    执行订阅
    参数：
      crontab_id：执行任务的ID
    """
  
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        #'cookie': site_cookie,
    }    
    
    #获取任务ID
    job_id = Job.objects.get(crontab_id=crontab_id)    
    ormdata_rule = Rule.objects.get(job_id = job_id.id)
    #订阅地址
    rss_url = ormdata_rule.config_id.url
    #站点信息
    siteinfo_id = ormdata_rule.config_id.siteinfo_id
    site_name = siteinfo_id.siteconfig_name
    site_name_cn = siteinfo_id.siteconfig_name_cn
    #关键字
    keyword = [x for x in ormdata_rule.keyword.split(',')]
    #码率
    rate = ormdata_rule.rate
    
    logger.info("-------------开始RSS订阅任务%s(%s)-------------------" % (site_name, site_name_cn))
    
    d = feedparser.parse(rss_url, request_headers=headers)
    #未获取返回状态
    if 'status' not in d:
        logger.error('请求RSS地址失败')
        return
    
    #匹配RSS过滤后发送
    send_data = []
    if d.status == 200:
        #entries 电影内容
        for i in d.entries:
            #标题 [Movie][Back to 1942 2012 V2 2160p WEB-DL H265 AAC-LeagueWEB][一九四二/温故1942/1942 | 类型: 剧情/历史/战争/灾难 主演: 张国立/张默/徐帆 [国语/中英双语硬字] | *4K* *V2高码*][16.35 GB]
            seed_name = i.title
            #种子类型 Movie
            seed_type = i.tags[0].term
            #种子页地址 https://lemonhd.org/details_movie.php?id=327311
            seed_link = i.link
            #'links': [{'rel': 'alternate', 'type': 'text/html', 'href': 'https://lemonhd.org/details_tv.php?id=328435'}, 
            #          {'length': '2543569030', 'type': 'application/x-bittorrent', 'href': 'https://lemonhd.org/download.php?id=328435&passkey=c1c6b3d5291bf330ffa9ad2872d52144', 
            #          'rel': 'enclosure'}
            #         ]
            #种子下载地址
            seed_download_url = i.links[1].href
            #种子大小 字节数
            seed_length = i.links[1].length
            #发布时间 Wed, 07 Sep 2022 14:27:09 +0800
            seed_published_time = i.published
            _TIME_FORMAT = "%a, %d %b %Y %H:%M:%S %z"
            #将字符串转换成datetime在格式化成需要的 2022-09-07 09:26:22
            seed_published_time = datetime.datetime.strptime(seed_published_time, _TIME_FORMAT).strftime('%Y-%m-%d %H:%M:%S') 
            #种子ID afe783da83684e92f5ff6a4c42fd11da216b77a2
            seed_hash_id = i.id
            
            seedinfo = None
            #确认无重复，则添加
            num = SeedInfo.objects.filter(seed_hash_id=seed_hash_id).filter(siteinfo_id=siteinfo_id).count()
            if num == 0:
                if keyword[0] == '':
                    
                    #未添加关键字则全部加入
                    if rate == 'all':
                        #码率为所有
                        seedinfo = SeedInfo.objects.create(seed_name = seed_name,
                                                seed_type = seed_type,
                                                seed_details_link = seed_link,
                                                seed_donwload_link = seed_download_url,
                                                seed_file_size = seed_length,
                                                seed_hash_id = seed_hash_id,
                                                seed_published_time = seed_published_time,
                                                siteinfo_id = siteinfo_id,
                                                rule_id = ormdata_rule
                                                )
                    else:
                        if rate in seed_name:
                            seedinfo = SeedInfo.objects.create(seed_name = seed_name,
                                                    seed_type = seed_type,
                                                    seed_details_link = seed_link,
                                                    seed_donwload_link = seed_download_url,
                                                    seed_file_size = seed_length,
                                                    seed_hash_id = seed_hash_id,
                                                    seed_published_time = seed_published_time,
                                                    siteinfo_id = siteinfo_id,
                                                    rule_id = ormdata_rule
                                                    )
                    #发送下载器
                    seed_download(seedinfo.id)
                    #将电影名加入发送
                    send_data.append(seed_name)
                else:
                    #通过匹配关键字添加
                    _name, num=process.extractOne(seed_name, keyword)
                    if num >= 50:
                        #匹配度大于50添加
                        if rate == 'all':
                            #码率为所有
                            seedinfo = SeedInfo.objects.create(seed_name = seed_name,
                                                    seed_type = seed_type,
                                                    seed_details_link = seed_link,
                                                    seed_donwload_link = seed_download_url,
                                                    seed_file_size = seed_length,
                                                    seed_hash_id = seed_hash_id,
                                                    seed_published_time = seed_published_time,
                                                    siteinfo_id = siteinfo_id,
                                                    rule_id = ormdata_rule
                                                    )
                        else:
                            if rate in seed_name:
                                seedinfo = SeedInfo.objects.create(seed_name = seed_name,
                                                        seed_type = seed_type,
                                                        seed_details_link = seed_link,
                                                        seed_donwload_link = seed_download_url,
                                                        seed_file_size = seed_length,
                                                        seed_hash_id = seed_hash_id,
                                                        seed_published_time = seed_published_time,
                                                        siteinfo_id = siteinfo_id,
                                                        rule_id = ormdata_rule
                                                        )
                        #发送下载器
                        seed_download(seedinfo.id)
                        #将电影名加入发送
                        send_data.append(seed_name)
                #发送通知
                send_msg(crontab_id, send_data, title='RSS订阅提示')
 
    return

def seed_download(seedinfo_id):
    """
    下载种子
    参数
    seedinfo_id rss订阅后存入数据库的id
    """
    
    ormdata_seedinfo = SeedInfo.objects.get(id = seedinfo_id)
    #下载连接
    seed_donwload_link = ormdata_seedinfo.seed_donwload_link
    #下载器类型
    download_type = ormdata_seedinfo.rule_id.tools_id.typed
    download_username = ormdata_seedinfo.rule_id.tools_id.username
    download_password = ormdata_seedinfo.rule_id.tools_id.password
    download_url = ormdata_seedinfo.rule_id.tools_id.url
    #下载目录
    download_dirname = ormdata_seedinfo.rule_id.tools_id.dirname
    #加入下载器后是否立刻下载
    is_paused = ormdata_seedinfo.rule_id.is_paused
    
    if download_dirname == "":
        download_dirname = None
        
    url_data = parseUrl(download_url)
    
    #保存加入下载器后返回的ID
    torrent_id = None
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
                          download_dir = download_dirname,
                          #paused = is_paused, #立刻下载,需要下载器开启默认下载才有效
                          )
            #获取种子id
            torrent_id = torrent.id
            #如果启动则下载
            if is_paused:
                c.start_torrent(torrent_id)
            
            ormdata_seedinfo.seed_torrent_id = torrent_id
            ormdata_seedinfo.seed_status = True
            ormdata_seedinfo.save()
        
        except Exception as e:
            print(e)

    elif download_type == 'qb':
        try:
            
            c = qbittorrentapi.Client(
                host=url_data['host'],
                port=url_data['port'],
                username=download_username,
                password=download_password,
            )
            
            torrent = c.torrents_add(seed_donwload_link,
                                     save_path=download_dirname,
                                     #is_paused=is_paused, #立刻下载
                                     )
            #获取种子id
            torrent_id = torrent.id
            #如果启动则下载
            if is_paused:
                c.start_torrent(torrent_id)
                
            ormdata_seedinfo.seed_torrent_id = torrent_id
            ormdata_seedinfo.seed_status = True
            ormdata_seedinfo.save()
            
        except Exception as e:
            print(e)         
        
    return