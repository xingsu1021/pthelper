# -*- coding:utf-8 -*- 
from django.conf import settings
import logging
import os
from bs4 import BeautifulSoup
import requests
import simplejson as json
import re
import time
from .utils import getSiteUrl, datetime2utc
#import ddddocr
from paddleocr import PaddleOCR
from thefuzz import fuzz
from thefuzz import process
import random
import datetime
#from cron.models import Log


logger = logging.getLogger('sign')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'

msg_ok = '<font color="#4CAF50">[签到成功]</font>'
msg_err_start = '<font color="#BF360C">[签到失败,错误:'
msg_err_end = ']</font>'
msg_reok = '<font color="#4CAF50">[重复签到]</font>'
msg_err_cookie = '<font color="#BF360C">[cookie失效]</font>'
msg_err_url = '<font color="#BF360C">[请求签到地址失败]</font>'
msg_unknow = '<font color="#BF360C">[未知错误]</font>'
msg_ok_visit = '<font color="#4CAF50">[模拟访问成功]</font>'

def signIngress(site_name, site_name_cn, site_url, site_cookie, sign_type):
    """
    签到站点匹配入口
    """
    
    if sign_type == 'hdchina':
        flag, data = hdchina(site_name, site_name_cn, site_url, site_cookie)
    elif sign_type == 'general':
        flag, data = general(site_name, site_name_cn, site_url, site_cookie)
    elif sign_type == 'pterclub':
        flag, data = pterclub(site_name, site_name_cn, site_url, site_cookie)
    elif sign_type == 'hdarea':
        flag, data = hdarea(site_name, site_name_cn, site_url, site_cookie)
    elif sign_type == 'hdcity':
        flag, data = hdcity(site_name, site_name_cn, site_url, site_cookie)
    elif sign_type == 'btschool':
        flag, data = btschool(site_name, site_name_cn, site_url, site_cookie)
    elif sign_type == 'hares':
        flag, data = hares(site_name, site_name_cn, site_url, site_cookie)
    elif sign_type == 'ttg':
        flag, data = ttg(site_name, site_name_cn, site_url, site_cookie)
    elif sign_type == 'pt52':
        flag, data = pt52(site_name, site_name_cn, site_url, site_cookie)
    elif sign_type == 'nosign':
        flag, data = nosign(site_name, site_name_cn, site_url, site_cookie)      
    elif sign_type == 'keepfrds':
        flag, data = keepfrds(site_name, site_name_cn, site_url, site_cookie)
    elif sign_type == 'tjupt':
        flag, data = tjupt(site_name, site_name_cn, site_url, site_cookie)
    elif sign_type == 'hd':
        flag, data = hd(site_name, site_name_cn, site_url, site_cookie)    
    elif sign_type == 'greatposterwall':
        flag, data = greatposterwall(site_name, site_name_cn, site_url, site_cookie)  
    elif sign_type == 'opencd':
        try:
            flag, data = opencd(site_name, site_name_cn, site_url, site_cookie)
        except Exception as e:
            logger.error(str(e))
            return False,'%s 数据异常' % site_name      
    elif sign_type == 'hdsky':
        try:
            flag, data = hdsky(site_name, site_name_cn, site_url, site_cookie)
        except Exception as e:
            logger.error(str(e))
            return False,'%s 数据异常' % site_name
    elif sign_type == 'haidan':
        flag, data = haidan(site_name, site_name_cn, site_url, site_cookie)     
    elif sign_type == 'ptsbao':
        flag, data = ptsbao(site_name, site_name_cn, site_url, site_cookie)   
    elif sign_type == 'ssd':
        flag, data = ssd(site_name, site_name_cn, site_url, site_cookie)   
    elif sign_type == 'u2':
        flag, data = u2(site_name, site_name_cn, site_url, site_cookie)          
    else:
        flag, data = (False,'%s 未匹配站点' % site_name) 
        
    return flag, data

def hdchina(site_name, site_name_cn, site_url, site_cookie):
    """
    瓷器签到
    """
    headers = {
        'user-agent': user_agent,
        'referer': site_url,
        'cookie': site_cookie
    }
    sign_url = 'https://hdchina.org/plugin_sign-in.php?cmd=signin'
    
    logger.info('--------------%s开始签到----------------' % site_name)
    
    try:
        
        session = requests.session()
        #请求首页获取csrf
        response = session.get(site_url, headers=headers, timeout=10)
        
        soup = BeautifulSoup(response.text, "lxml")
        csrf = soup.find('meta',{'name':'x-csrf'})
        csrf = csrf.attrs['content']
        
        data = {  
            'csrf': csrf
            #'csrf': 'e3a2895bb529c567fb2aae3723a97ba9144c1c5c'
        }
        
        response = session.post(sign_url, headers=headers, data=data) 
        logger.info(response.text)
        if response.status_code == 200:
            try:
                #正确请求，得到json字符串
                response_msg = json.loads(response.text)
                if response_msg['state'] == 'success':
                    #signindays = response_msg['signindays']
                    #integral = response_msg['integral']
                    msg = "%s(%s) %s" % (site_name, site_name_cn, msg_ok)
                else:
                    #crsf不正确
                    if 'msg' in response_msg:
                        msg = "%s(%s) %s%s%s" % (site_name,site_name_cn, msg_err_start, response_msg['msg'], msg_err_end)
                        return False, msg 
                    else:
                        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_reok)
            except:
                #失败，返回html
                msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                return False, msg
            
                ##cookie失效的抓取(待后期确认页面内容)
                #soup = BeautifulSoup(response.text, "lxml")
                #error = soup.findAll('h1')
                #if len(error) != 0:
                    #if '未登录' in str(error[0]):
                        #msg = "%s(%s) cookie失效" % (site_name,site_name_cn)                
                        #return False, msg 
            
            return True, msg
        else:
            msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
            logger.error('--------------%s----------------' % site_name)
            logger.error(response.text)
            
            return False, msg
        
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error('--------------%s----------------' % site_name)
        logger.error(str(e))
        
        return False, msg
        
def hdarea(site_name, site_name_cn, site_url, site_cookie):
    """
    高清视界签到
    """
    headers = {
        'user-agent': user_agent,
        'referer': site_url,
        'cookie': site_cookie
    }
    sign_url = 'https://www.hdarea.co/sign_in.php'
    
    logger.info('--------------%s开始签到----------------' % site_name)
    
    try:
        data = {  
            'action': 'sign_in'
        }
                
        response = requests.post(sign_url, headers=headers, data=data) 
        
        if response.status_code == 200:
            try:
                response_msg = response.text
                if response_msg.strip() == '':
                    msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                    return False, msg
                else:

                    if '重复签到' in response_msg:
                        msg = "%s(%s) %s " % (site_name,site_name_cn, msg_reok)
                    else:
                        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_ok)
                    
                return True, msg
            except:
                #失败，返回html
                msg = "%s(%s) %s" % (site_name,site_name_cn, msg_err_cookie)
                return False, msg
                        
            return True, msg
        else:
            msg = "%s(%s) %s" % (site_name,site_name_cn, msg_err_url)
            logger.error('--------------%s----------------' % site_name)
            logger.error(response.text)
            
            return False, msg
        
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error('--------------%s----------------' % site_name)
        logger.error(str(e))
        
        return False, msg

def pterclub(site_name, site_name_cn, site_url, site_cookie):
    """
    猫站签到
    """
    headers = {
        'user-agent': user_agent,
        'referer': site_url,
        'cookie': site_cookie
    }
    #获取网站url,不带/结尾
    sign_url = getSiteUrl(site_url) + '/attendance-ajax.php'
    
    logger.info('--------------%s开始签到----------------' % site_name)
    
    try:
        
        response = requests.get(sign_url, headers=headers) 
        
        if response.status_code == 200:
            try:
                #正确请求，得到json字符串
                response_msg = json.loads(response.text)

                if response_msg['status'] == '1':
                    #message = response_msg['message']
                    msg = "%s(%s) %s" % (site_name, site_name_cn, msg_ok)

                else:
                    msg = "%s(%s) %s" % (site_name, site_name_cn, msg_reok)

            except:
                #失败，返回html
                msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                return False, msg
            
            return True, msg
        else:
            msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
            logger.error('--------------%s----------------' % site_name)
            logger.error(response.text)
            
            return False, msg
        
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error('--------------%s----------------' % site_name)
        logger.error(str(e))
        
        return False, msg

def hdcity(site_name, site_name_cn, site_url, site_cookie):
    """
    城市签到
    """
    
    headers = {
        'user-agent': user_agent,
        'referer': site_url,
        'cookie': site_cookie
    }
    
    #获取网站url,不带/结尾
    sign_url = getSiteUrl(site_url) + '/sign'
    
    logger.info('--------------%s开始签到----------------' % site_name)
    
    try:
        response = requests.get(sign_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            
            #二次请求
            response = requests.get(sign_url, headers=headers, timeout=10)
            
            html = response.text

            soup = BeautifulSoup(html, "lxml")
            
            form = soup.findAll('form',{'action':'signinhandler'})
            
            if len(form) >= 1:
                #cookie失效
                msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                return False, msg                
            else:
                tables = soup.findAll('div', {'class':'container'})
            
                check_sign = tables[1].find('span',{'class':'colored'}).get_text()
                if '已经签过' in check_sign:
                    #data = tables[1].find('div',{'class':'col-md-12'}).p.get_text()
                    #msg = "%s(%s) %s" % (site_name,site_name_cn, data.replace('<p>','').replace('</p>',''))
                    msg = "%s(%s) %s" % (site_name,site_name_cn, msg_ok)
                else:
                    msg = "%s(%s) %s" % (site_name,site_name_cn, msg_unknow)
                    return False, msg
                                
            return True, msg
        else:
            msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
            logger.error('--------------%s----------------' % site_name)
            logger.error(response.text)
            
            return False, msg
                
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error(str(e))
        
        return False, msg
        
def btschool(site_name, site_name_cn, site_url, site_cookie):
    """
    学校签到
    """
    
    headers = {
        'user-agent': user_agent,
        'referer': site_url,
        'cookie': site_cookie
    }
    
    #获取网站url,不带/结尾
    sign_url = getSiteUrl(site_url) + '/index.php?action=addbonus'
    
    logger.info('--------------%s开始签到----------------' % site_name)
    
    #s = requests.session()
    #cookie = cookie_parse(site_cookie)
    #s.headers.update(headers)
    #s.cookies.update(cookie)    
    try:
        response = requests.get(sign_url, headers=headers, timeout=10)
        #response = s.get(sign_url)
        #print(response.text)
        
        if response.status_code == 200:
            
            html = response.text
            
            soup = BeautifulSoup(html, "lxml")
            font = soup.findAll('font',{'color':'white'})

            if len(font) != 0:
                #msg = "%s(%s) %s" % (site_name,site_name_cn,font[0].get_text())
                msg = "%s(%s) %s" % (site_name,site_name_cn, msg_ok)
            else:
                tables = soup.findAll('table', {'id':'info_block'})
            
                if len(tables) != 0:     
                    msg = "%s(%s) %s" % (site_name,site_name_cn, msg_reok)
                else:
                    msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                    return False, msg                    
            
            return True, msg
        else:
            msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
            logger.error('--------------%s----------------' % site_name)
            logger.error(response.text)
            
            return False, msg
                
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error(str(e))
        
        return False, msg   
    
def hares(site_name, site_name_cn, site_url, site_cookie):
    """
    白兔签到
    {'code': 0, 'msg': '签到成功', 'count': '1', 
    'datas': {'id': 1361, 'uid': 1505, 'added': '2022-09-08 05:30:15', 'points': 175, 'total_points': 9010, 'days': 34, 'total_days': 305, 'added_time': '05:30:15', 'is_updated': 1}}
    """
    
    headers = {
        'user-agent': user_agent,
        'referer': site_url,
        'cookie': site_cookie,
        'Accept': 'application/json'
    }
    
    #获取网站url,不带/结尾
    sign_url = getSiteUrl(site_url) + '/attendance.php?action=sign'
    
    logger.info('--------------%s开始签到----------------' % site_name)
    
    try:
        response = requests.get(sign_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            try:
                
                #正确请求，得到json字符串
                response_msg = json.loads(response.text)
                logger.info(response_msg)
                if response_msg['code'] == 0:
                    sign_data = response_msg['datas']
                    uid = sign_data['uid']
                    #签到魔力
                    points = sign_data['points']
                    #连续签到天数
                    days = sign_data['days']
                    
                    #msg = "%s(%s) 签到成功,连续签到%s,今日签到得%s积分" % (site_name,site_name_cn,str(days),str(points))
                    msg = "%s(%s) %s" % (site_name,site_name_cn, msg_ok)
                else:
                    if '已经签到' in response_msg['msg']:
                        msg = "%s(%s) %s " % (site_name,site_name_cn, msg_reok)
                    else:                    
                        #msg = "%s(%s) 提示：%s" % (site_name,site_name_cn,response_msg['msg'])
                        msg = "%s(%s) %s%s%s" % (site_name,site_name_cn, msg_err_start, response_msg['msg'], msg_err_end)

                return True, msg
            except:
                #失败，返回html
                msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                return False, msg            
        else:
            msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
            logger.error('--------------%s----------------' % site_name)
            logger.error(response.text)
            
            return False, msg
                
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error(str(e))
        
        return False, msg
    

def general(site_name, site_name_cn, site_url, site_cookie):
    """
    常规签到
    """
    
    headers = {
        'user-agent': user_agent,
        'referer': site_url,
        'cookie': site_cookie
    }
    
    #获取网站url,不带/结尾
    sign_url = getSiteUrl(site_url) + '/attendance.php'
    
    logger.info('--------------%s开始签到----------------' % site_name)
    
    try:
        response = requests.get(sign_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            
            html = response.text
            
            #需要安装pip install lxml
            soup = BeautifulSoup(html, "lxml")

            for j in soup.findAll('table', {'class':'main'}):
                if '签到成功' in str(j) or '簽到成功' in str(j):
                    #print(i)
                    #info = i.findAll('td', {'class':'text'})
                    #d = j.find('p')
                    #替换掉p标签,tg不支持
                    msg = "%s(%s) %s" % (site_name, site_name_cn, msg_ok)
         
                elif '已经签到' in str(j) or '已經簽到' in str(j):
                    msg = "%s(%s) %s" % (site_name, site_name_cn, msg_reok)

            #cookie失效的抓取
            error_table = soup.findAll('table', {'class':'mainouter'})
            
            if len(error_table) != 0:
                fail_msg = error_table[0].find('p')
                
                if '错误' in str(fail_msg) or '錯誤' in str(fail_msg):
                    msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                    return False, msg
            
            return True, msg
        else:
            msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
            logger.error('--------------%s----------------' % site_name)
            logger.error(response.text)
            
            return False, msg
                
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error(str(e))
        
        return False, msg
        
def nosign(site_name, site_name_cn, site_url, site_cookie):
    """
    无签到，直接访问
    """
    
    headers = {
        'user-agent': user_agent,
        'cookie': site_cookie
    }
    
    #获取网站url,不带/结尾
    sign_url = getSiteUrl(site_url) + '/index.php'
    
    logger.info('--------------%s开始签到----------------' % site_name)
    
    try:
        response = requests.get(sign_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            #需要安装pip install lxml
            soup = BeautifulSoup(response.text, "lxml")
            
            tables = soup.findAll('table', {'id':'info_block'})
        
            if len(tables) != 0:
                
                #span获取有2个，一个为用户信息，一个为信箱信息
                #info = tables[0].findAll('span', {'class':'medium'})
                #user_info = info[0]
                
                ##print(user_info)
                ##print("-------------")
                ##用户详情链接
                #user_info_link = user_info.a.attrs['href']
                ##用户名
                #user_name = user_info.a.get_text()
                ##魔力值
                #bonus = user_info.find('font',{'class':'color_bonus'}).nextSibling.nextSibling.nextSibling.get_text().replace(']:','')
                ##分享率
                #ratio = user_info.find('font',{'class':'color_ratio'}).nextSibling.get_text()
                ##上传量
                #uploaded = user_info.find('font',{'class':'color_uploaded'}).nextSibling.get_text()
                ##下载量
                #downloaded = user_info.find('font',{'class':'color_downloaded'}).nextSibling.get_text()
                
                ##print(user_info.find('font',{'class':'color_active'}).get_text(),user_info.find('img',{'class':'arrowup'}).nextSibling.get_text(),user_info.find('img',{'class':'arrowdown'}).nextSibling.get_text())
                ##print("-------------")
                #message_info = info[1]
                #new_message = message_info.a.nextSibling.get_text()
                #print('用户详情链接:%s' % user_info_link)
                #msg = "%s(%s) 魔力:%s,分享率:%s,新消息:%s" % (site_name,site_name_cn, bonus,ratio,new_message)
                msg = "%s(%s) %s" % (site_name,site_name_cn, msg_ok_visit)
                
                return True, msg
            else:
                msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                return False, msg
                
        else:
            msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
            logger.error('--------------%s----------------' % site_name)
            logger.error(msg)
            
            return False, msg
            
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error('--------------%s----------------' % site_name)
        logger.error(str(e))
        
        return False, msg    
    
def keepfrds(site_name, site_name_cn, site_url, site_cookie):
    """
    keepfrds 朋友
    """
    
    headers = {
        'user-agent': user_agent,
        'cookie': site_cookie
    }
    
    #获取网站url,不带/结尾
    sign_url = getSiteUrl(site_url) + '/index.php'
    
    logger.info('--------------%s开始签到----------------' % site_name)
    
    try:
        response = requests.get(sign_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            #需要安装pip install lxml
            soup = BeautifulSoup(response.text, "lxml")
            
            tables = soup.findAll('table', {'id':'info_block'})
        
            if len(tables) != 0:
                
                #获取有3个，0:所有，1:为用户信息，2:为信箱信息
                tds = tables[0].findAll('td')          
                td1 = tds[1].findAll('span',{'class':'nowrap'})
                            
                #用户详情链接
                user_info_link = td1[0].a.attrs['href']        
                #用户名
                user_name = td1[0].a.get_text()

                #魔力值
                bonus = tds[1].find('font',{'class':'color_bonus'}).nextSibling.nextSibling.nextSibling.get_text().replace(']:','')
                #分享率
                ratio =  tds[1].find('font',{'class':'color_ratio'}).nextSibling.get_text()
                #上传量
                uploaded =  tds[1].find('font',{'class':'color_uploaded'}).nextSibling.get_text()
                #下载量
                downloaded =  tds[1].find('font',{'class':'color_downloaded'}).nextSibling.get_text()
                
                message_info = tds[2]
                new_message = message_info.a.get_text()
                if new_message == "":
                    new_message = 0
                #msg = "%s(%s) 魔力:%s,分享率:%s,新消息:%s" % (site_name,site_name_cn, bonus,ratio,new_message)
                msg = "%s(%s) %s" % (site_name,site_name_cn, msg_ok_visit)
                
                return True, msg
            else:
                msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                return False, msg
                
        else:
            msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
            logger.error('--------------%s----------------' % site_name)
            logger.error(msg)
            
            return False, msg
            
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error('--------------%s----------------' % site_name)
        logger.error(str(e))
        
        return False, msg    
    
def tjupt(site_name, site_name_cn, site_url, site_cookie):
    """
    tjupt 北洋园
    """
    
    headers = {
        'user-agent': user_agent,
        'cookie': site_cookie
    }
    

    
    try:
        #验证码签到执行3次验证
        for i in range(3):
            #验证成功退出
            if i > 2:
                msg = "%s(%s) %s连续3次电影匹配失败%s" % (site_name,site_name_cn, msg_err_start, msg_err_end) 
                return False, msg
            
            #获取网站url,不带/结尾
            sign_url = getSiteUrl(site_url) + '/attendance.php'
            
            logger.info('--------------%s开始签到----------------' % site_name)        
            response = requests.get(sign_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                #需要安装pip install lxml
                soup = BeautifulSoup(response.text, "lxml")
                
                tables = soup.findAll('table', {'class':'captcha'})
                
                answer_data = {}
                if len(tables) != 0:
                    
                    #获取图片链接
                    img_src = tables[0].find('img')
                    img = img_src.attrs['src']
                    logger.info(img)
                    
                    #获取答案列表
                    img_data = tables[0].findAll('input',{'name':'answer'})
                    logger.info(img_data)
                    for i in img_data:
                        answer_data[i.nextSibling.get_text()] = i.attrs['value']
                
                    logger.info(answer_data)
                    #use_gpu= False 使用CPU预加载，不用GPU
                    #lang支持ch, en, french, german, korean, japan
                    #use_angle_cls = True 使用分类模型，不存在则自动下载
                    ocr = PaddleOCR(lang="ch",use_angle_cls = True,use_gpu= False, show_log=False)
                    #获取所有电影名称
                    #a = answer_data.keys()
                    result = ocr.ocr(img, cls=True)
                    #保存最终图片电影名称
                    answer_data_result = ""
                    #保存匹配比率
                    ratio = 0
                    for line in result:
                        #得到图片解释的汉字
                        d = line[1][0]
                        #print(d)
                        logger.info("图片电影名: " + d)
                        #limit返回结果数量
                        #f = process.extract(d, a, limit=2)
                        #只返回一个结果
                        f, num = process.extractOne(d, answer_data.keys())
                        logger.info("模糊匹配电影名: " + f + "-" + str(num))
                        if num == 0:
                            continue
                        
                        if num == 100:
                            answer_data_result = f
                            ratio = 100
                            break
                        elif num >= 75 and ratio <= 75:
                            answer_data_result = f
                            ratio = num
                        elif num >= 50 and ratio <= 50:
                            answer_data_result = f
                            ratio = num
                        elif num >= 45 and ratio <= 45:
                            answer_data_result = f   
                            ratio = num
                                                                        
                    logger.info("结果匹配电影名: " + answer_data_result + "-" + str(ratio))
                    if answer_data_result != "":
                        
                        data = {'answer': answer_data[answer_data_result],
                                'submit': "提交"
                                }
                        
                        response = requests.post("https://tjupt.org/attendance.php", headers=headers, data=data, timeout=10)
                        if '签到成功' in response.text:
                            msg = "%s(%s) %s" % (site_name, site_name_cn, msg_ok)
                            return True, msg
                        else:
                            logger.error(response.text)
                            msg = "%s(%s) %s" % (site_name,site_name_cn, msg_unknow)
                            return False, msg
                    else:
                        msg = "%s(%s) %s无法匹配电影名称%s" % (site_name,site_name_cn, msg_err_start, msg_err_end)
                        return False, msg                    
                        
                else:
                    
                    if '今日已签到' in response.text:
                        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_reok)
                        return True, msg
                    else:
                        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                        return False, msg
                    
            else:
                msg = "%s(%s) %s" % (site_name,site_name_cn,msg_err_url)
                logger.error('--------------%s----------------' % site_name)
                logger.error(msg)
                
                return False, msg
            
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error('--------------%s----------------' % site_name)
        logger.error(str(e))
        
        return False, msg        
    
def tjupt_old(site_name, site_name_cn, site_url, site_cookie):
    """
    tjupt 北洋园（废弃）
    """
    
    headers = {
        'user-agent': user_agent,
        'cookie': site_cookie
    }
    
    #获取网站url,不带/结尾
    sign_url = getSiteUrl(site_url) + '/index.php'
    
    logger.info('--------------%s开始签到----------------' % site_name)
    
    try:
        response = requests.get(sign_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            #需要安装pip install lxml
            soup = BeautifulSoup(response.text, "lxml")
            
            tables = soup.findAll('table', {'id':'info_block'})
            if len(tables) != 0:
                #获取有1个
                tds = tables[0].findAll('td')
                td1 = tds[1].findAll('span',{'class':'nowrap'})
                
                #用户详情链接
                user_info_link = td1[0].a.attrs['href']        
                #用户名
                user_name = td1[0].a.get_text()
        
                #魔力值
                bonus = tds[1].find('a',{'href':'mybonusapps.php'}).nextSibling.get_text().replace(']:','')
        
                #上传量
                uploaded =  tds[1].find('font',{'class':'color_uploaded'}).nextSibling.get_text()
                #HR积分
                ratio =  tds[1].find('a',{'href':'/hnr_bonus.php'}).nextSibling.get_text().replace(']:','')
        
                new_message = tds[2].a.nextSibling.get_text()

                if new_message == "":
                    new_message = 0
                msg = "%s(%s) 魔力:%s,HR积分:%s,新消息:%s" % (site_name,site_name_cn, bonus,ratio,new_message)
                
                return True, msg
    
            else:
                msg = "%s(%s) 登录网站失败,cookie已经失效" % (site_name,site_name_cn)
                return False, msg
            
        else:
            msg = "%s(%s) 请求地址失败" % (site_name,site_name_cn)
            logger.error('--------------%s----------------' % site_name)
            logger.error(msg)
            
            return False, msg
            
    except Exception as e:
        msg = "%s(%s) 请求失败" % (site_name,site_name_cn)
        logger.error('--------------%s----------------' % site_name)
        logger.error(str(e))
        
        return False, msg    
    
def hd(site_name, site_name_cn, site_url, site_cookie):
    """
    海带，直接访问
    """
    
    headers = {
        'user-agent': user_agent,
        'cookie': site_cookie
    }
    
    #获取网站url,不带/结尾
    sign_url = getSiteUrl(site_url) + '/index.php'
    
    logger.info('--------------%s开始签到----------------' % site_name)
    
    try:
        response = requests.get(sign_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            #需要安装pip install lxml
            soup = BeautifulSoup(response.text, "lxml")
            
            div = soup.findAll('div', {'class':'site-topbar'})
            
            if len(div) != 0:
                #上传，下载，分享
                nav = div[0].findAll('div', {'class':'topbar-nav'})
            
                navs = nav[0].findAll('a')
                #上传量
                uploaded = navs[0].get_text().strip()
                #下载量
                downloaded= navs[1].get_text().strip()
                #分享率
                ratio = navs[2].get_text().strip()
                
                #用户信息，信箱
                info = div[0].findAll('div', {'class':'topbar-info'})
                infos = info[0].findAll('a')
                #print(infos)
                #用户详情链接
                user_info_link = infos[0].attrs['href']
                #魔力值
                bonus = infos[1].get_text().strip()
                #邀请数量
                invite = infos[2].get_text().strip()        
                #消息
                new_message = infos[3].get_text().strip()

                #msg = "%s(%s) 魔力:%s,分享率:%s,新消息:%s" % (site_name,site_name_cn, bonus,ratio,new_message)
                msg = "%s(%s) %s" % (site_name,site_name_cn, msg_ok)
                
                return True, msg
            else:
                msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                return False, msg
                
        else:
            msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
            logger.error('--------------%s----------------' % site_name)
            logger.error(msg)
            
            return False, msg
            
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error('--------------%s----------------' % site_name)
        logger.error(str(e))
        
        return False, msg    

def ttg(site_name, site_name_cn, site_url, site_cookie):
    """
    听听歌,签到
    """
    
    headers = {
        'user-agent': user_agent,
        'referer': site_url,
        'cookie': site_cookie
    }
    
    #获取网站url,不带/结尾
    sign_url = getSiteUrl(site_url) + '/signed.php'
    
    logger.info('--------------%s开始签到----------------' % site_name)
    
    try:
        #首先请求获取token
        response = requests.get(site_url, headers=headers, timeout=10)
        if response.status_code == 200:
            #TTG返回页面乱码，需要处理
            html = response.text.encode(response.encoding).decode('utf-8')
            try:
                b = re.search(r'signed_timestamp.*\}',html).group()
                data = b.replace('}','')
                signed_timestamp = data.split(',')[0].split(':')[-1].strip().replace("\"","")
                signed_token = data.split(',')[1].split(':')[-1].strip().replace("\"","")

                data = {
                    'signed_timestamp':signed_timestamp,
                    'signed_token':signed_token
                }

                response = requests.post(sign_url, headers=headers, data=data)
                response_msg = response.text.encode(response.encoding).decode('utf-8')
                if '已签到过' in response_msg:
                    #msg = "%s(%s) 您今天已经签到过了，请勿重复签到" % (site_name,site_name_cn)
                    msg = "%s(%s) %s" % (site_name,site_name_cn, msg_reok)
                else:
                    msg = "%s(%s) %s" % (site_name,site_name_cn, msg_ok)
                
            except:
                msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                return False, msg
            
            return True, msg
        else:
            msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
            logger.error('--------------%s----------------' % site_name)
            logger.error(msg)
            
            return False, msg
            
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error('--------------%s----------------' % site_name)
        logger.error(str(e))
        
        return False, msg    

def pt52(site_name, site_name_cn, site_url, site_cookie):
    """
    52pt,签到
    """
    
    headers = {
        'user-agent': user_agent,
        'referer': site_url,
        'cookie': site_cookie
    }
    
    #获取网站url,不带/结尾
    sign_url = getSiteUrl(site_url) + '/bakatest.php'
    
    logger.info('--------------%s开始签到----------------' % site_name)
    
    try:
        #获取问题id
        response = requests.get(sign_url, headers=headers, timeout=10)
        html = response.text
        
        soup = BeautifulSoup(html, "lxml")
        input = soup.findAll('input', {'name':'questionid'})
        
        if len(input) != 0:
            #上传，下载，分享
            value = input[0].attrs['value']
        
            data =  {'wantskip': '不会',
                     'choice': [1],
                     'questionid': value
                    }
            #请求签到
            response = requests.post(sign_url, headers=headers, data=data, timeout=10)
            
            html = response.text
            soup = BeautifulSoup(html, "lxml")
            font = soup.findAll('font', {'color':'white'})
            
            if len(font) != 0:
                sign_msg = font[0].get_text().strip()

                msg = "%s(%s) %s" % (site_name,site_name_cn, msg_ok )
            else:
                #msg = "%s(%s) 未知错误" % (site_name,site_name_cn)
                msg = "%s(%s) %s" % (site_name,site_name_cn, msg_unknow)
                logger.error('--------------%s----------------' % site_name)
                return False, msg  
            
            return True, msg
        else:
            font = soup.findAll('font', {'color':'white'})
            
            if len(font) != 0:            
                msg = "%s(%s) %s" % (site_name, site_name_cn, msg_reok)
            else:
                #input和font都没有找到，说明cookie失效
                msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                return False, msg                 
            
        return True, msg
            
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error('--------------%s----------------' % site_name)
        logger.error(str(e))
        
        return False, msg    

def greatposterwall(site_name, site_name_cn, site_url, site_cookie):
    """
    海豹，直接访问
    """
    
    headers = {
        'user-agent': user_agent,
        'cookie': site_cookie
    }
    
    #获取网站url,不带/结尾
    sign_url = getSiteUrl(site_url) + '/index.php'
    
    logger.info('--------------%s开始签到----------------' % site_name)
    
    try:
        response = requests.get(sign_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            
            soup = BeautifulSoup(response.text, "lxml")
            #常规
            #ul1 = soup.findAll('ul', {'class':'Header-infoMiddle Header-stat'})
            #积分,用户链接
            #ul2 = soup.findAll('ul', {'class':'Header-infoRight Header-quickaction'})
            #我的信箱
            ul1 = soup.findAll('a', {'class':'DropdownMenu-item is-inbox'})
            
            
            if len(ul1) != 0:
                
                #value = ul1[0].findAll('span',{'class':'Header-statValue'})
        
                ##上传量
                #uploaded = value[0].get_text().strip()
                ##下载量
                #downloaded= value[1].get_text().strip()
                ##分享率
                #ratio = value[2].get_text().strip()
                ##合格分享率
                #required_ratio = value[3].get_text().strip()
                ##令牌
                #fl_token = value[4].get_text().strip()
                ##积分
                #value_bonus = ul2[0].findAll('a',{'class':'Header-quickactionLink tooltip'})
                #bonus = value_bonus[1].attrs['title'].replace("积分 ","").replace("(","").replace(")","")

                #value_user_info_link = ul2[0].findAll('a',{'class':'Header-moreLink DropdownMenu-item is-profile'})
                ##用户链接
                #user_info_link = value_user_info_link[0].attrs['href']
                #msg = "%s(%s) 积分:%s,分享率:%s,令牌:%s" % (site_name,site_name_cn, bonus,ratio,fl_token)
                msg = "%s(%s) %s" % (site_name,site_name_cn, msg_ok_visit)
                
                return True, msg
            
            else:
                msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                return False, msg
                
        else:
            msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
            logger.error('--------------%s----------------' % site_name)
            logger.error(msg)
            
            return False, msg
            
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error('--------------%s----------------' % site_name)
        logger.error(str(e))
        
        return False, msg    
    
def opencd(site_name, site_name_cn, site_url, site_cookie):
    """
    皇后，签到
    """
    

    headers = {
        'user-agent': user_agent,
        'referer': site_url,
        'cookie': site_cookie
    }
    
    image_code_name = os.path.join(settings.TMP_LOG_DIR,'opencd_code.png')
    
    logger.info('--------------%s开始签到----------------' % site_name)
    
    ocr = PaddleOCR(use_gpu = False, 
                    show_log=False, 
                    rec_model_dir=os.path.join(settings.BASE_DIR, 'paddleocr', 'captcha_rec_model'),
                    rec_char_dict_path = os.path.join(settings.BASE_DIR, 'paddleocr', 'captcha_rec_model_dic.txt'),
                    use_angle_cls=True
                    )

    try:
        session = requests.session()
        
        #校验确认是否已经签到
        response = session.get("https://open.cd/index.php", headers=headers, timeout=10)
        if '查看簽到記錄' in response.text:
            msg = "%s(%s) %s" % (site_name,site_name_cn, msg_reok)
            return True, msg
        
        #验证码签到执行3次验证
        for i in range(3):
            #验证成功退出
            if i > 2:
                return False, "%s(%s) 错误:连续3次验证码失败" % (site_name,site_name_cn) 
            
            response = session.get("https://open.cd/plugin_sign-in.php", headers=headers, timeout=10)
            if response.status_code == 200:
                html = response.text
                #print(html)
                soup = BeautifulSoup(html, "lxml")
                value = soup.findAll('input',{'name':'imagehash'})
                if len(value) != 0:
                    
                    imagehash = value[0].attrs['value']
                    #https://open.cd/image.php?action=regimage&imagehash=672effec852f76345b025ea97f5a4e7e
                    img_url = "https://open.cd/image.php?action=regimage&imagehash=" + imagehash
                    logger.info(img_url)
                    
                    response = session.get(img_url, headers=headers, timeout=10)
                    #获取文件内容 #text（字符串） content（二进制） json（对象）
                    #image_data = response.content
                    with open(image_code_name, "wb") as fp:
                        fp.write(response.content)
                    
                    data_ocr = ocr.ocr(image_code_name, det=False, rec=True, cls=True)[0][0]

                    logger.info(data_ocr)
                    
                    #验证码不足6未跳过
                    if len(data_ocr) != 6 :
                        continue
                    
                    data = {'imagehash': imagehash,
                            'imagestring': data_ocr
                            }
                    response = session.post("https://open.cd/plugin_sign-in.php?cmd=signin", headers=headers, data=data, timeout=10)
                    logger.info(response.text)
                    
                    result = json.loads(response.text)
    
                    if result['state'] == 'success':
                        signindays = result['signindays']
                        integral = result['integral']
                        #msg = "%s(%s) 连续签到%s,本次获得%s" % (site_name,site_name_cn, signindays,integral)
                        msg = "%s(%s) %s" % (site_name,site_name_cn, msg_ok)
                        return True, msg
                    else:
                        if 'msg' in result:
                            #msg = "%s(%s) 签到失败：%s" % (site_name,site_name_cn, result['msg'])
                            msg = "%s(%s) %s%s%s" % (site_name,site_name_cn, msg_err_start, result['msg'],msg_err_end)
                        else:
                            #msg = "%s(%s) 签到失败" % (site_name,site_name_cn)
                            logger.error(str(result))
                            msg = "%s(%s) %s" % (site_name,site_name_cn, msg_unknow)
                        if i > 2:
                            return False, msg
    
                else:
                    msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                    return False, msg
                    
            else:
                msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
                logger.error('--------------%s----------------' % site_name)
                logger.error(msg)
                
                return False, msg
            
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error('--------------%s----------------' % site_name)
        logger.error(str(e))
        
        return False, msg    
    
def hdsky(site_name, site_name_cn, site_url, site_cookie):
    """
    天空，签到
    """
    
    headers = {
        'user-agent': user_agent,
        'referer': site_url,
        'cookie': site_cookie
    }
    
    sign_url = 'https://hdsky.me/image_code_ajax.php'
    
    data = {  
        'action': 'new'
    }

    image_code_name = os.path.join(settings.TMP_LOG_DIR,'hdsky_code.png')
    
    logger.info('--------------%s开始签到----------------' % site_name)
 
    #ocr = ddddocr.DdddOcr(show_ad=False,old=True)
    ocr = PaddleOCR(use_gpu = False, 
                    show_log=False, 
                    rec_model_dir=os.path.join(settings.BASE_DIR, 'paddleocr', 'captcha_rec_model'),
                    rec_char_dict_path = os.path.join(settings.BASE_DIR, 'paddleocr', 'captcha_rec_model_dic.txt'),
                    use_angle_cls=True
                    )
    try:
        
        #session = requests.session()
        
        #验证码签到执行3次验证
        for i in range(3):
            logger.info('开始循环%s--------->' % str(i))
            #验证成功退出
            if i > 2:
                #print('i--------->',i)
                return False, "%s(%s) 错误:连续3次验证码失败" % (site_name,site_name_cn)
            
            response = requests.post(sign_url, headers=headers, data=data, timeout=10)
            logger.info(response.text)
            if response.status_code == 200:
                result = json.loads(response.text)
                if result['success']:
                    code = result['code']
                    #拼接验证码图片
                    hdsky_image_url = 'https://hdsky.me/image.php?action=regimage&imagehash=' + code
                    response = requests.get(hdsky_image_url, headers=headers, timeout=10)
                    with open(image_code_name, "wb") as fp:
                        fp.write(response.content)
                    
                    #with open(image_code_name, 'rb') as f:
                        #image = f.read()              
                        
                    #data_ocr = ocr.classification(image)
                    
                    data_ocr = ocr.ocr(image_code_name, det=False, rec=True, cls=True)[0][0]
                    logger.info(data_ocr)
                    
                    #验证码不足6未跳过
                    if len(data_ocr) != 6 :
                        continue
                    
                    data = {'action': 'showup',
                            'imagehash': code,
                            'imagestring': data_ocr
                            }
                    response = requests.post("https://hdsky.me/showup.php", headers=headers, data=data, timeout=10)
                    logger.info(response.text)
                    try:
                        result = json.loads(response.text)
                        
                        if result['success']:
                            #msg = "%s(%s) 连续签到%s" % (site_name,site_name_cn, result['message'])
                            msg = "%s(%s) %s" % (site_name,site_name_cn, msg_ok)
                            return True, msg                            
                        else:
                            #false的情况存在无message
                            if 'message' in result:
                                if 'date_unmatch' == result['message']:
                                    #msg = "%s(%s) 您今天已经签到过了，请勿重复签到" % (site_name,site_name_cn)
                                    msg = "%s(%s) %s" % (site_name,site_name_cn, msg_reok)
                                    return True, msg
                                else:
                                    #invalid_imagehash说明数据验证码错误
                                    #msg = "%s(%s) 错误:%s" % (site_name,site_name_cn, result['message'])
                                    msg = "%s(%s) %s%s%s" % (site_name,site_name_cn, msg_err_start, result['message'], msg_err_end)
    
                                    #超过2次退出
                                    if i > 2:
                                        return False,msg
                                    else:
                                        continue
                            else:
                                logger.info("no message")
                                continue

                    except:
                        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                        return False, msg  
                else:
                    #存在获取数据失败
                    #超过2次退出
                    if i > 2:
                        return False, "%s(%s) 错误:连续3次验证码失败" % (site_name,site_name_cn)
                    else:
                        continue
    
            else:
                msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
                logger.error('--------------%s----------------' % site_name)
                logger.error(msg)
                
                return False, msg
            
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error('--------------%s----------------' % site_name)
        logger.error(str(e))
        
        return False, msg    
    
def haidan(site_name, site_name_cn, site_url, site_cookie):
    """
    海胆，签到,由于海胆请求后返回登录页面，因此先验证数据
    """
        
    headers = {
        'user-agent': user_agent,
        'referer': site_url,
        'cookie': site_cookie
    }
    
    sign_url = 'https://www.haidan.video/signin.php'
    
    url = getSiteUrl(site_url) + '/index.php'

    logger.info('--------------%s开始签到----------------' % site_name)
    
    try:
        
        session = requests.session()
        
        response = session.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, "lxml")
            #常规
            div = soup.findAll('div', {'class':'userinfo-half'})
        
            if len(div) != 0:
                
                #用户连接
                user_info = div[0].findAll('span',{'class':'nowrap username-center'})
                user_info_link = user_info[0].a.attrs['href']
                
                #签到状态
                sign_status = div[0].findAll('input',{'class':'dt_button'})
                sign_status = sign_status[0].attrs['value']

                #详细信息
                value = div[1].findAll('div',{'class':'user_item'})
                #积分
                bonus = value[0].span.get_text().strip()

                #魔力值
                magic_num = value[1].span.get_text().strip()

                #分享率
                ratio = value[2].font.nextSibling.get_text().strip()

                #上传量
                uploaded = value[3].font.nextSibling.get_text().strip()

                #下载量
                downloaded= value[4].font.nextSibling.get_text().strip()

                #收件箱
                message = value[6].a.nextSibling.get_text().strip()

                if '已经' not in sign_status:
                    #开始签到
                    response = requests.get(sign_url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:

                        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_ok)
                        return True, msg
                    else:
                        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_unknow)
                        return False, msg                        
                else:
                    msg = "%s(%s) %s" % (site_name, site_name_cn, msg_reok)
                    return True, msg

            else:
                msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                return False, msg
                
        else:
            msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
            logger.error('--------------%s----------------' % site_name)
            logger.error(msg)
            
            return False, msg
            
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error('--------------%s----------------' % site_name)
        logger.error(str(e))
        
        return False, msg    
    
def ptsbao(site_name, site_name_cn, site_url, site_cookie):
    """
    烧包签到
    """
    
    headers = {
        'user-agent': user_agent,
        'referer': site_url,
        'cookie': site_cookie
    }
    
    #获取网站url,不带/结尾
    sign_url = getSiteUrl(site_url) + '/index.php'
    
    logger.info('--------------%s开始签到----------------' % site_name)
    
    try:
        response = requests.get(sign_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            
            html = response.text
        
            soup = BeautifulSoup(html, "lxml")
            
            tables = soup.findAll('table', {'id':'info_block'})
        
            if len(tables) != 0:
                
                info = tables[0].findAll('span', {'class':'medium'})
                user_info = info[0]

                #用户详情链接
                user_info_link = user_info.a.attrs['href']
                #用户名
                user_name = user_info.a.get_text()

                #魔力值
                data = re.search(r']：(.*)<font class="color_bonus">',str(user_info)).group().strip()
                bonus = data.split(' ')[0].replace(']：','')

                #分享率
                ratio = user_info.find('font',{'class':'color_ratio'}).nextSibling.get_text().strip()

                #上传量
                uploaded = user_info.find('font',{'class':'color_uploaded'}).nextSibling.get_text().strip()

                #下载量
                downloaded = user_info.find('font',{'class':'color_downloaded'}).nextSibling.get_text().strip()

                message_info = info[1]
                new_message = message_info.a.nextSibling.get_text().strip()
                #print('用户详情链接:%s' % user_info_link)
                #msg = "魔力:%s,分享率:%s,新消息:%s" % (bonus,ratio,new_message)
                msg = "%s(%s) %s" % (site_name, site_name_cn, msg_ok)
                
                return True, msg
            else:
                msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                return False, msg
        else:
            msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
            logger.error('--------------%s----------------' % site_name)
            logger.error(response.text)
            
            return False, msg
                
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error(str(e))
        
        return False, msg
    
def ssd(site_name, site_name_cn, site_url, site_cookie):
    """
    无签到，春天cmct
    """
    
    headers = {
        'user-agent': user_agent,
        'cookie': site_cookie
    }
    
    #获取网站url,不带/结尾
    sign_url = getSiteUrl(site_url) + '/index.php'
    
    logger.info('--------------%s开始签到----------------' % site_name)
    
    try:
        response = requests.get(sign_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            #需要安装pip install lxml
            soup = BeautifulSoup(response.text, "lxml")
            
            tables = soup.findAll('div', {'id':'info_block'})
        
            if len(tables) != 0:
                
                #span获取有2个，一个为用户信息，一个为信箱信息
                info = tables[0].findAll('span', {'class':'medium'})
                user_info = info[0]
                
                #print(user_info)
                #print("-------------")
                #用户详情链接
                user_info_link = user_info.a.attrs['href']
                #用户名
                user_name = user_info.a.get_text()
                #魔力值
                bonus = user_info.find('a',{'href':'mybonus.php'}).get_text().split(':')[-1]
                #分享率
                ratio = user_info.find('font',{'class':'color_ratio'}).nextSibling.get_text()
                #上传量
                uploaded = user_info.find('font',{'class':'color_uploaded'}).nextSibling.get_text()
                #下载量
                downloaded = user_info.find('font',{'class':'color_downloaded'}).nextSibling.get_text()

                message_info = info[1].find('a',{'href':'messages.php'}).nextSibling.get_text()
                #msg = "%s(%s) 魔力:%s,分享率:%s,新消息:%s" % (site_name,site_name_cn, bonus.strip(), ratio.strip(), message_info.strip())
                msg = "%s(%s) %s" % (site_name,site_name_cn, msg_ok_visit)
                
                return True, msg
            else:
                msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                return False, msg
                
        else:
            msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
            logger.error('--------------%s----------------' % site_name)
            logger.error(msg)
            
            return False, msg
            
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error('--------------%s----------------' % site_name)
        logger.error(str(e))
        
        return False, msg    
    
def u2(site_name, site_name_cn, site_url, site_cookie):
    """
    签到 动漫花园
    """
    
    headers = {
        'user-agent': user_agent,
        'cookie': site_cookie
    }
    
    #获取网站url,不带/结尾
    sign_url = getSiteUrl(site_url) + '/showup.php'
    
    logger.info('--------------%s开始签到----------------' % site_name)
    #u2以utc0为时区，因此签到时间按utc+8时区为早上8点
    now = datetime.datetime.now()
    utc_now = datetime2utc(now)
    #判断北京日期和utc日期都为今天
    if utc_now.day != now.day and utc_now.hour >= 0:
        msg = "%s(%s) %s%s%s" % (site_name, site_name_cn, msg_err_start,'签到时间未到',msg_err_end)
        return False, msg
        
    try:
        session = requests.session()
        response = session.get(sign_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            #需要安装pip install lxml
            soup = BeautifulSoup(response.text, "lxml")
            
            tables = soup.findAll('table', {'class':'captcha'})
            #print(tables)
            data = {}
            captcha = []
            data['message'] = '注意：回答按钮点击时即提交，手滑损失自负~'
            if len(tables) != 0:
                
                #获取所有input
                info = tables[0].findAll('input')
                for i in info:
                    #print(i)
                    #获取input的名称,用于post使用
                    name = i.attrs['name']
                    if name == 'req':
                        data['req'] = i.attrs['value']
                    elif name == 'hash':
                        data['hash'] = i.attrs['value']
                    elif name == 'form':
                        data['form'] = i.attrs['value']
                    elif 'captcha' in name:
                        captcha.append({i.attrs['name']:i.attrs['value']})
                        
                #随机选择一个作为答案
                answer = random.choice(captcha)
                #取出键值对
                key,value = answer.popitem()
                data[key] = value
                #不返回任何消息
                response = session.post("https://u2.dmhy.org/showup.php?action=show", headers=headers, data=data, timeout=10)
                logger.info(data)
                #暂停5秒
                time.sleep(5)
                #确认是否签到成功
                response = session.get(sign_url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, "lxml")
                h3 = soup.findAll('h3', {'align':'center'})
                if '今天已签到' in h3[0].get_text():
                    msg = "%s(%s) %s" % (site_name,site_name_cn, msg_ok)
                    return True, msg
                else:
                    msg = "%s(%s) %s" % (site_name,site_name_cn, msg_unknow)
                    return False, msg
                
            else:
                #u2以utc0为时区，因此实际签到时间需要北京时间8点后才可以，通过日志确认是否签到过
                #获取今天日期
                #today = datetime.datetime.today()                
                #num = Log.objects.filter(site_name='u2').filter(created_at__date=today).count()
                h3 = soup.findAll('h3', {'align':'center'})
                #if '今天已签到' in h3[0].get_text() and num != 0:
                if '今天已签到' in h3[0].get_text():
                    msg = "%s(%s) %s" % (site_name, site_name_cn, msg_reok)
                    return True, msg
                #elif '今天已签到' in h3[0].get_text() and num == 0:
                    #msg = "%s(%s) %s%s%s" % (site_name, site_name_cn, msg_err_start,'签到错误',msg_err_end)
                    #return False, msg                
                else:
                    msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_cookie)
                    return False, msg
                
        else:
            msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
            logger.error('--------------%s----------------' % site_name)
            logger.error(msg)
            
            return False, msg
            
    except Exception as e:
        msg = "%s(%s) %s" % (site_name, site_name_cn, msg_err_url)
        logger.error('--------------%s----------------' % site_name)
        logger.error(str(e))
        
        return False, msg    