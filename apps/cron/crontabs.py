# coding=utf-8
from django.conf import settings
import requests
import datetime
from urllib import parse
import os
import logging
from bs4 import BeautifulSoup

from common.utils import send_email,send_telegram,send_iyuu, send_enwechat
from common.sites_sign import signIngress
from sites.models import SiteConfig, SiteInfo
from .models import Job, Log
from notify.models import NotifyConfig
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
    send_msg(crontab_id, send_data)
    
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
    send_msg(crontab_id, send_data)
    
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
        send_msg(crontab_id, send_data)
    
    return

def send_msg(crontab_id = None, send_data = []):
    """
    发送消息
    """
    logger.info("-------------send_data-------------------")
    logger.info(",".join(send_data))
    #获取对应任务ID的记录详情
    notify_ormdata = Job.objects.get(crontab_id = crontab_id)
    if 'iyuu' in notify_ormdata.notifys:
        
        iyuu_ormdata = NotifyConfig.objects.get(name='iyuu')
        
        flag,msg = send_iyuu(iyuu_ormdata.iyuu_key, send_data)
        logger.info("-------------iyuu-------------------")
        logger.info(msg)
        
    if 'telegram' in notify_ormdata.notifys:
        tg_ormdata = NotifyConfig.objects.get(name='telegram')
        flag,msg = send_telegram(tg_ormdata.tg_chat_id,tg_ormdata.tg_token,send_data)
        logger.info("-------------telegram-------------------")
        logger.info(msg)
        
    if 'email' in notify_ormdata.notifys:
        email_ormdata = NotifyConfig.objects.get(name='email')
        
        receiver_users = [x for x in email_ormdata.receive_user.split(',')]
        flag,msg = send_email(email_ormdata.mail_type,email_ormdata.smtp_user,email_ormdata.smtp_password,receiver_users,send_data)
        logger.info("-------------email-------------------")
        logger.info(msg)   
        
    if 'enwechat' in notify_ormdata.notifys:
        enwechat_ormdata = NotifyConfig.objects.get(name='enwechat')
        
        receiver_users = [x for x in enwechat_ormdata.receive_user.split(',')]
        flag, msg = send_enwechat(corp_id=enwechat_ormdata.enwechat_corp_id, 
                                 agent_id=enwechat_ormdata.enwechat_agent_id, 
                                 agent_secret=enwechat_ormdata.enwechat_agent_secret,
                                 user_ids = receiver_users,
                                 send_data = send_data
                                 )
        
        logger.info("-------------enwechat-------------------")
        logger.info(msg)
        
    return