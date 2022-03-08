# coding=utf-8
import requests
import datetime
from urllib import parse
import os
import logging
from bs4 import BeautifulSoup

from common.utils import send_email,send_telegram,send_iyuu
from common.sites_sign import hdchina, general,noSign,keepfrds,tjupt,pterclub,hdarea,hdcity,btschool,hares,hd,ttg,pt52,greatposterwall,hdsky,opencd,haidan,ptsbao
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
     
            #headers = {
                #'user-agent': user_agent,
                #'referer': site_url,
                #'cookie': site_cookie
            #}
            if site_name == 'hdchina':
                flag, data = hdchina(site_name, site_name_cn, site_url, site_cookie)
            elif site_name in ['hdfans','1ptba','ptchina','3wmg','discfan','hddolby','hdatmos','soulvoice',
                               'pthome','hdtime','hdzone','htpt','audiences','nicept','hdhome','pttime',
                               'lemonhd','ourbits','asf']:
                flag, data = general(site_name, site_name_cn, site_url, site_cookie)
            elif site_name == 'pterclub':
                flag, data = pterclub(site_name, site_name_cn, site_url, site_cookie)
            elif site_name == 'hdarea':
                flag, data = hdarea(site_name, site_name_cn, site_url, site_cookie)
            elif site_name == 'hdcity':
                flag, data = hdcity(site_name, site_name_cn, site_url, site_cookie)
            elif site_name == 'btschool':
                flag, data = btschool(site_name, site_name_cn, site_url, site_cookie)
            elif site_name == 'hares':
                flag, data = hares(site_name, site_name_cn, site_url, site_cookie)
            elif site_name == 'totheglory':
                flag, data = ttg(site_name, site_name_cn, site_url, site_cookie)
            elif site_name == '52pt':
                flag, data = pt52(site_name, site_name_cn, site_url, site_cookie)
            elif site_name in ['beitai','msg','hdmayi','oshen','avgv','eastgame','et8','itzmx']:
                flag, data = noSign(site_name, site_name_cn, site_url, site_cookie)      
            elif site_name == 'keepfrds':
                flag, data = keepfrds(site_name, site_name_cn, site_url, site_cookie)
            elif site_name == 'tjupt':
                flag, data = tjupt(site_name, site_name_cn, site_url, site_cookie)
            elif site_name == 'hd':
                flag, data = hd(site_name, site_name_cn, site_url, site_cookie)    
            elif site_name == 'greatposterwall':
                flag, data = greatposterwall(site_name, site_name_cn, site_url, site_cookie)  
            elif site_name == 'open':
                flag, data = opencd(site_name, site_name_cn, site_url, site_cookie)
            elif site_name == 'hdsky':
                flag, data = hdsky(site_name, site_name_cn, site_url, site_cookie)
            elif site_name == 'haidan':
                flag, data = haidan(site_name, site_name_cn, site_url, site_cookie)     
            elif site_name == 'ptsbao':
                flag, data = ptsbao(site_name, site_name_cn, site_url, site_cookie)             
            else:
                flag, data = (False,'%s 未匹配站点' % site_name)
            
            #print(site_name,data)
            try:
                Log.objects.create(name = '签到',type_id = 1000, crontab_id = crontab_id, site_name=site_name, message = data, status = flag)
            except:
                logger.error("%s(%s)数据返回出错" % (site_name, site_name_cn))

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

