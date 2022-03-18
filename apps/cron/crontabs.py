# coding=utf-8
import requests
import datetime
from urllib import parse
import os
import logging
from bs4 import BeautifulSoup

from common.utils import send_email,send_telegram,send_iyuu
from common.sites_sign import signIngress
from sites.models import SiteConfig, SiteInfo
from .models import Job, Log
from notify.models import NotifyConfig


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'

def sign(crontab_id):
    """
    执行签到
    参数：
      crontab_id：执行任务的ID
    """

    logger = logging.getLogger('sign')
    
    #保存最后发送的结果
    send_data = []
    site_count = SiteInfo.objects.count()
    if site_count == 0:
        send_data.append('未配置任何站点')
    else:
        #获取所有已经配置的站点
        sites = SiteInfo.objects.all()
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

