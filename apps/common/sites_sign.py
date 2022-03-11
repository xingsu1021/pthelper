# -*- coding:utf-8 -*- 
from django.conf import settings
import logging
import os
from bs4 import BeautifulSoup
import requests
import simplejson as json
import re
import time
from .utils import getSiteUrl
import ddddocr

logger = logging.getLogger('sign')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'

def signIngress(site_name, site_name_cn, site_url, site_cookie):
    """
    签到站点匹配入口
    """
    
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
        try:
            flag, data = hdsky(site_name, site_name_cn, site_url, site_cookie)
        except Exception as e:
            logger.error(str(e))
            return False,'%s 数据异常' % site_name
    elif site_name == 'haidan':
        flag, data = haidan(site_name, site_name_cn, site_url, site_cookie)     
    elif site_name == 'ptsbao':
        flag, data = ptsbao(site_name, site_name_cn, site_url, site_cookie)             
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
        
        #请求首页获取csrf
        #response = requests.get(site_url, headers=headers, timeout=10)
        
        #soup = BeautifulSoup(response.text, "lxml")
        #csrf = soup.find('meta',{'name':'x-csrf'})
        #csrf = csrf.attrs['content']
        
        data = {  
            #'csrf': csrf
            'csrf': 'e3a2895bb529c567fb2aae3723a97ba9144c1c5c'
        }
        
        response = requests.post(sign_url, headers=headers, data=data) 
        logger.info(response.text)
        if response.status_code == 200:
            try:
                #正确请求，得到json字符串
                response_msg = json.loads(response.text)
                if response_msg['state'] == 'success':
                    signindays = response_msg['signindays']
                    integral = response_msg['integral']
                    msg = "%s(%s) 签到成功,连续签到%s,今日签到得%s积分" % (site_name,site_name_cn,str(signindays),str(integral))
                else:
                    #crsf不正确
                    if 'msg' in response_msg:
                        msg = "%s(%s) 错误：%s" % (site_name,site_name_cn,response_msg['msg'])
                        return False, msg 
                    else:
                        msg = "%s(%s) 您今天已经签到过了，请勿重复签到" % (site_name,site_name_cn)
            except:
                #失败，返回html
                msg = "%s(%s) cookie失效" % (site_name,site_name_cn)
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
            msg = "%s(%s) 请求签到地址失败" % (site_name,site_name_cn)
            logger.error('--------------%s----------------' % site_name)
            logger.error(response.text)
            
            return False, msg
        
    except Exception as e:
        msg = "%s(%s) 请求地址失败" % (site_name,site_name_cn)
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
                    msg = "%s(%s) cookie失效" % (site_name,site_name_cn)
                    return False, msg
                else:

                    if '重复签到' in response_msg:
                        msg = "%s(%s) 请不要重复签到哦！" % (site_name,site_name_cn)
                    else:
                        msg = "%s(%s) 签到成功,%s" % (site_name,site_name_cn,response_msg)
                    
                return True, msg
            except:
                #失败，返回html
                msg = "%s(%s) cookie失效" % (site_name,site_name_cn)
                return False, msg
                        
            return True, msg
        else:
            msg = "%s(%s) 请求签到地址失败" % (site_name,site_name_cn)
            logger.error('--------------%s----------------' % site_name)
            logger.error(response.text)
            
            return False, msg
        
    except Exception as e:
        msg = "%s(%s) 请求地址失败" % (site_name,site_name_cn)
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
                    message = response_msg['message']
                    msg = "%s(%s) 签到成功,%s" % (site_name,site_name_cn,message.replace('<p>','').replace('</p>',''))

                else:
                    msg = "%s(%s) 您今天已经签到过了，请勿重复签到" % (site_name,site_name_cn)

            except:
                #失败，返回html
                msg = "%s(%s) cookie失效" % (site_name,site_name_cn)
                return False, msg
            
            return True, msg
        else:
            msg = "%s(%s) 请求签到地址失败" % (site_name,site_name_cn)
            logger.error('--------------%s----------------' % site_name)
            logger.error(response.text)
            
            return False, msg
        
    except Exception as e:
        msg = "%s(%s) 请求地址失败" % (site_name,site_name_cn)
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
                msg = "%s(%s) cookie失效" % (site_name,site_name_cn)
                return False, msg                
            else:
                tables = soup.findAll('div', {'class':'container'})
            
                check_sign = tables[1].find('span',{'class':'colored'}).get_text()
                if '已经签过' in check_sign:
                    data = tables[1].find('div',{'class':'col-md-12'}).p.get_text()
                    msg = "%s(%s) %s" % (site_name,site_name_cn, data.replace('<p>','').replace('</p>',''))
                else:
                    msg = "%s(%s) 未知错误" % (site_name,site_name_cn)
                    return False, msg
                                
            return True, msg
        else:
            msg = "%s(%s) 请求签到地址失败" % (site_name,site_name_cn)
            logger.error('--------------%s----------------' % site_name)
            logger.error(response.text)
            
            return False, msg
                
    except Exception as e:
        msg = "%s(%s) 请求失败" % (site_name,site_name_cn)
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
                msg = "%s(%s) %s" % (site_name,site_name_cn,font[0].get_text())
            else:
                tables = soup.findAll('table', {'id':'info_block'})
            
                if len(tables) != 0:     
                    msg = "%s(%s) 您今天已经签到过了，请勿重复签到" % (site_name,site_name_cn)
                else:
                    msg = "%s(%s) cookie失效" % (site_name,site_name_cn)
                    return False, msg                    
            
            return True, msg
        else:
            msg = "%s(%s) 请求签到地址失败" % (site_name,site_name_cn)
            logger.error('--------------%s----------------' % site_name)
            logger.error(response.text)
            
            return False, msg
                
    except Exception as e:
        msg = "%s(%s) 请求失败" % (site_name,site_name_cn)
        logger.error(str(e))
        
        return False, msg   
    
def hares(site_name, site_name_cn, site_url, site_cookie):
    """
    白兔签到
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
            
            soup = BeautifulSoup(html, "lxml")
            #script = soup.findAll('script')
            #sign_data = script[-1]
            #print(sign_data)
            pattern = re.compile(r"layer.confirm\('(.*)',")
            script = soup.find("script", text=pattern)
        
            if script != None:
                
                data = re.search(r"layer.confirm\('(.*),",str(script)).group()
                sign_data = data.replace("layer.confirm('",'').replace("。',",'')
                
                if '签到获得' in sign_data:
                    #替换掉p标签,tg不支持
                    msg = "%s(%s) %s" % (site_name,site_name_cn,sign_data)
         
                else:
                    msg = "%s(%s) 您今天已经签到过了，请勿重复签到" % (site_name,site_name_cn)
            else:
                msg = "%s(%s) cookie失效" % (site_name,site_name_cn)
                return False, msg

            return True, msg
        else:
            msg = "%s(%s) 请求签到地址失败" % (site_name,site_name_cn)
            logger.error('--------------%s----------------' % site_name)
            logger.error(response.text)
            
            return False, msg
                
    except Exception as e:
        msg = "%s(%s) 请求失败" % (site_name,site_name_cn)
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
                    d = j.find('p')
                    #替换掉p标签,tg不支持
                    msg = "%s(%s) %s" % (site_name,site_name_cn,str(d).replace('<p>','').replace('</p>',''))
         
                elif '已经签到' in str(j) or '已經簽到' in str(j):
                    msg = "%s(%s) 您今天已经签到过了，请勿重复签到" % (site_name,site_name_cn)

            #cookie失效的抓取
            error_table = soup.findAll('table', {'class':'mainouter'})
            
            if len(error_table) != 0:
                fail_msg = error_table[0].find('p')
                
                if '错误' in str(fail_msg) or '錯誤' in str(fail_msg):
                    msg = "%s(%s) cookie失效" % (site_name,site_name_cn)
                    return False, msg
            
            return True, msg
        else:
            msg = "%s(%s) 请求签到地址失败" % (site_name,site_name_cn)
            logger.error('--------------%s----------------' % site_name)
            logger.error(response.text)
            
            return False, msg
                
    except Exception as e:
        msg = "%s(%s) 请求失败" % (site_name,site_name_cn)
        logger.error(str(e))
        
        return False, msg
        
def noSign(site_name, site_name_cn, site_url, site_cookie):
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
                info = tables[0].findAll('span', {'class':'medium'})
                user_info = info[0]
                
                #print(user_info)
                #print("-------------")
                #用户详情链接
                user_info_link = user_info.a.attrs['href']
                #用户名
                user_name = user_info.a.get_text()
                #魔力值
                bonus = user_info.find('font',{'class':'color_bonus'}).nextSibling.nextSibling.nextSibling.get_text().replace(']:','')
                #分享率
                ratio = user_info.find('font',{'class':'color_ratio'}).nextSibling.get_text()
                #上传量
                uploaded = user_info.find('font',{'class':'color_uploaded'}).nextSibling.get_text()
                #下载量
                downloaded = user_info.find('font',{'class':'color_downloaded'}).nextSibling.get_text()
                
                #print(user_info.find('font',{'class':'color_active'}).get_text(),user_info.find('img',{'class':'arrowup'}).nextSibling.get_text(),user_info.find('img',{'class':'arrowdown'}).nextSibling.get_text())
                #print("-------------")
                message_info = info[1]
                new_message = message_info.a.nextSibling.get_text()
                #print('用户详情链接:%s' % user_info_link)
                msg = "%s(%s) 魔力:%s,分享率:%s,新消息:%s" % (site_name,site_name_cn, bonus,ratio,new_message)
                
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
                msg = "%s(%s) 魔力:%s,分享率:%s,新消息:%s" % (site_name,site_name_cn, bonus,ratio,new_message)
                
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
    
def tjupt(site_name, site_name_cn, site_url, site_cookie):
    """
    tjupt 北洋园
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

                msg = "%s(%s) 魔力:%s,分享率:%s,新消息:%s" % (site_name,site_name_cn, bonus,ratio,new_message)
                
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
                    msg = "%s(%s) 您今天已经签到过了，请勿重复签到" % (site_name,site_name_cn)
                else:
                    msg = "%s(%s) %s" % (site_name,site_name_cn, response_msg)
                
            except:
                msg = "%s(%s) 登录网站失败,cookie已经失效" % (site_name,site_name_cn)
                return False, msg
            
            return True, msg
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

                msg = "%s(%s) %s" % (site_name,site_name_cn,sign_msg )
            else:
                msg = "%s(%s) 未知错误" % (site_name,site_name_cn)
                logger.error('--------------%s----------------' % site_name)
                return False, msg  
            
            return True, msg
        else:
            font = soup.findAll('font', {'color':'white'})
            
            if len(font) != 0:            
                msg = "%s(%s) 您今天已经签到过了，请勿重复签到" % (site_name,site_name_cn)
            else:
                #input和font都没有找到，说明cookie失效
                msg = "%s(%s) 登录网站失败,cookie已经失效" % (site_name,site_name_cn)
                return False, msg                 
            
        return True, msg
            
    except Exception as e:
        msg = "%s(%s) 请求失败" % (site_name,site_name_cn)
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
            ul1 = soup.findAll('ul', {'class':'Header-infoMiddle Header-stat'})
            #积分,用户链接
            ul2 = soup.findAll('ul', {'class':'Header-infoRight Header-quickaction'})
            
            
            if len(ul1) != 0:
                
                value = ul1[0].findAll('span',{'class':'Header-statValue'})
        
                #上传量
                uploaded = value[0].get_text().strip()
                #下载量
                downloaded= value[1].get_text().strip()
                #分享率
                ratio = value[2].get_text().strip()
                #合格分享率
                required_ratio = value[3].get_text().strip()
                #令牌
                fl_token = value[4].get_text().strip()
                #积分
                value_bonus = ul2[0].findAll('a',{'class':'Header-quickactionLink tooltip'})
                bonus = value_bonus[1].attrs['title'].replace("积分 ","").replace("(","").replace(")","")

                value_user_info_link = ul2[0].findAll('a',{'class':'Header-moreLink DropdownMenu-item is-profile'})
                #用户链接
                user_info_link = value_user_info_link[0].attrs['href']
                msg = "%s(%s) 积分:%s,分享率:%s,令牌:%s" % (site_name,site_name_cn, bonus,ratio,fl_token)
                
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
    
    ocr = ddddocr.DdddOcr(show_ad=False,old=True)
    try:
        #验证码签到执行3次验证
        for i in range(3):
            #验证成功退出
            if i > 2:
                return False, "%s(%s) 错误:连续3次验证码失败" % (site_name,site_name_cn) 
            
            response = requests.get("https://open.cd/plugin_sign-in.php", headers=headers, timeout=10)
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
                    
                    response = requests.get(img_url, headers=headers, timeout=10)
                    #获取文件内容 #text（字符串） content（二进制） json（对象）
                    #image_data = response.content
                    with open(image_code_name, "wb") as fp:
                        fp.write(response.content)
                    
                    with open(image_code_name, 'rb') as f:
                        image = f.read()              
                        
                    data_ocr = ocr.classification(image)
                    logger.info(data_ocr)
                
                    data = {'imagehash': imagehash,
                            'imagestring': data_ocr
                            }
                    response = requests.post("https://open.cd/plugin_sign-in.php?cmd=signin", headers=headers, data=data, timeout=10)
                    logger.info(response.text)
                    
                    result = json.loads(response.text)
    
                    if result['state'] == 'success':
                        signindays = result['signindays']
                        integral = result['integral']
                        msg = "%s(%s) 连续签到%s,本次获得%s" % (site_name,site_name_cn, signindays,integral)
                        return True, msg
                    else:
                        msg = "%s(%s) 签到失败：%s" % (site_name,site_name_cn, result['msg'])
                        if i > 2:
                            return False, msg
    
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
 
    ocr = ddddocr.DdddOcr(show_ad=False,old=True)
    try:
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
                    
                    with open(image_code_name, 'rb') as f:
                        image = f.read()              
                        
                    data_ocr = ocr.classification(image)
                    logger.info(data_ocr)
    
                    data = {'action': 'showup',
                            'imagehash': code,
                            'imagestring': data_ocr
                            }
                    response = requests.post("https://hdsky.me/showup.php", headers=headers, data=data, timeout=10)
                    logger.info(response.text)
                    try:
                        result = json.loads(response.text)
                        
                        if result['success']:
                            msg = "%s(%s) 连续签到%s" % (site_name,site_name_cn, result['message'])
                            return True, msg                            
                        else:
                            #false的情况存在无message
                            if 'message' in result:
                                if 'date_unmatch' == result['message']:
                                    msg = "%s(%s) 您今天已经签到过了，请勿重复签到" % (site_name,site_name_cn)
                                    return True, msg
                                else:
                                    #invalid_imagehash说明数据验证码错误
                                    msg = "%s(%s) 错误:%s" % (site_name,site_name_cn, result['message'])
    
                                    #超过2次退出
                                    if i > 2:
                                        return False,msg
                                    else:
                                        continue
                            else:
                                logger.info("no message")
                                continue

                    except:
                        msg = "%s(%s) 登录网站失败,cookie已经失效" % (site_name,site_name_cn)
                        return False, msg  
                else:
                    #存在获取数据失败
                    time.sleep(5)
                    continue
                    
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
        
        response = requests.get(url, headers=headers, timeout=10)
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

                        msg = "%s(%s) 签到成功" % (site_name,site_name_cn)
                        return True, msg
                    else:
                        msg = "%s(%s) 签到失败" % (site_name,site_name_cn)
                        return False, msg                        
                else:
                    msg = "%s(%s) 您今天已经签到过了，请勿重复签到" % (site_name,site_name_cn)
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
                msg = "魔力:%s,分享率:%s,新消息:%s" % (bonus,ratio,new_message)
                
                return True, msg
            else:
                msg = "%s(%s) 登录网站失败,cookie已经失效"
                return False, msg
        else:
            msg = "%s(%s) 请求签到地址失败" % (site_name,site_name_cn)
            logger.error('--------------%s----------------' % site_name)
            logger.error(response.text)
            
            return False, msg
                
    except Exception as e:
        msg = "%s(%s) 请求失败" % (site_name,site_name_cn)
        logger.error(str(e))
        
        return False, msg