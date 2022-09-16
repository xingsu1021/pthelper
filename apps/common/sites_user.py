# -*- coding:utf-8 -*- 
from django.conf import settings
import logging
import os
from bs4 import BeautifulSoup
import requests
import simplejson as json
import re
import time
from .utils import getSiteUrl, parseUrl


logger = logging.getLogger('user')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'


def userIngress(site_name, site_name_cn, site_url, site_cookie, sign_type):
    """
    站点用户匹配入口
    """
    if sign_type in ['general','opencd','nosign']:
        flag, data = general(site_name, site_name_cn, site_url, site_cookie)
    else:
        flag, data = (False,'%s 未匹配站点' % site_name)
        
    return flag, data

    if sign_type == 'hdchina':
        flag, data = hdchina(site_name, site_name_cn, site_url, site_cookie)
    elif sign_type in ['general','opencd','nosign']:
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
     
    elif sign_type == 'keepfrds':
        flag, data = keepfrds(site_name, site_name_cn, site_url, site_cookie)
    elif sign_type == 'tjupt':
        flag, data = tjupt(site_name, site_name_cn, site_url, site_cookie)
    elif sign_type == 'hd':
        flag, data = hd(site_name, site_name_cn, site_url, site_cookie)    
    elif sign_type == 'greatposterwall':
        flag, data = greatposterwall(site_name, site_name_cn, site_url, site_cookie)  
     
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
    else:
        flag, data = (False,'%s 未匹配站点' % site_name) 
        
    return flag, data
        
def RepresentsInt(s):
    """
    判断是否整形
    """
    try: 
        int(s)
        return True
    except ValueError:
        return False
    
def general(site_name, site_name_cn, site_url, site_cookie):
    """
    通用获取
    """
    
    headers = {
        'user-agent': user_agent,
        'cookie': site_cookie
    }
    
    logger.info('--------------%s开始获取用户信息----------------' % site_name)

    #获取网站url,不带/结尾
    url = getSiteUrl(site_url) + '/index.php'
    
    session = requests.session()
    
    data = {}
    #初始0,有些站点可能没有积分
    data['score'] = 0
    try:
        response = session.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            #需要安装pip install lxml
            soup = BeautifulSoup(response.text, "lxml")
            
            href = soup.find_all(href=re.compile("userdetails.php"), limit=1)
            
            #print(ul)
            if len(href) != 0:
                
                #用户详情链接
                user_info_link = href[0].attrs['href']
                #print(user_info_link)
                
                #获取用户ID
                user_id = parseUrl(user_info_link)['query'].get('id',[])[0]
                
                data['user_id'] = user_id
                
                userdetails_url = site_url + "/userdetails.php?id=%s" % user_id
        
                response = session.get(userdetails_url, headers=headers, timeout=10)
                #print(response.text)
                soup = BeautifulSoup(response.text, "lxml")
                
                td = soup.findAll('td', string="用户名", limit=1)
                if len(td) != 0:
                    user_name = td[0].nextSibling.get_text()
                else:
                    user_name = href[0].get_text()
                    if len(user_name) == 0:
                        td = soup.findAll('span', {'class':'nowrap'}, limit=1)
                        user_name = td[0].get_text()
                data['user_name'] = user_name
                
                td = soup.findAll('td', string="加入日期", limit=1)
                create_time = re.sub("\(.*\)",'', td[0].nextSibling.get_text().strip())
                data['create_time'] = create_time
                
                td = soup.findAll('td', string=["等级","等級"], limit=1)
                level = re.sub("\(.*\)",'',td[0].nextSibling.get_text().strip())
                if level == "":
                    level = re.sub("\(.*\)",'',td[0].nextSibling.img.attrs['title'])
                data['level'] = level
                
                td = soup.findAll('td', string=["邀请","邀請","剩余邀请量"], limit=1)
                #删除非数字字符(获取字符串的整数) \D：表示非数字
                num = re.sub(r'\D+', '', td[0].nextSibling.get_text())
                if RepresentsInt(num):
                    data['invite'] = num
                else:
                    data['invite'] = 0         
                
                td = soup.findAll('td', string="做种积分", limit=1)
                try:
                    score = re.sub("\(.*\)",'', td[0].nextSibling.get_text())
                    score = re.sub("\[.*\]",'', score)
                except:
                    #无做种积分
                    score = '0'
                data['score'] = score.strip()
                
                td = soup.findAll('td', string="核心数据", limit=1)
                if len(td) != 0:
                    #pttime
                    ratio = td[0].nextSibling.font.get_text()
                    data['ratio'] = ratio
                    #分隔4个连续空格['', '上传量:  21.367TB\n            ', '下载量:  5.072TB', '魔力值:  6469.8']
                    d =td[0].nextSibling.font.nextSibling.get_text().split(u'\xa0\xa0\xa0\xa0')
                    upload = d[1].split(':')[-1].replace('\\n','').strip()
                    data['upload'] = upload
                    download = d[2].split(':')[-1].strip()
                    data['download'] = download
                    bonus = d[3].split(':')[-1].strip()
                    data['bonus'] = bonus
                            
                else:
                    #常规
                    td = soup.findAll('td', string=["奶糖","魔力值"], limit=1)
                    bonus = td[0].nextSibling.get_text()
                    data['bonus'] = bonus
                    
                    td = soup.findAll('td', string=["上传量","上傳量"], limit=1)
                    try:
                        upload = td[0].nextSibling.get_text()
                    except:
                        td = soup.findAll('strong', string=["上传量","上傳量"], limit=1)
                        upload = re.sub("\(.*\)",'', td[0].nextSibling.get_text().split(':')[-1])
                    data['upload'] = upload.strip()
                    
                    td = soup.findAll('td', string=["下载量","下載量"], limit=1)
                    try:
                        download = td[0].nextSibling.get_text()
                    except:
                        td = soup.findAll('strong', string=["下载量","下載量"], limit=1)
                        download = re.sub("\(.*\)",'', td[0].nextSibling.get_text().split(':')[-1])
                    data['download'] = download.strip()
                    
                    td = soup.findAll('td', string="分享率", limit=1)
                    if len(td) != 0:
                        ratio = td[0].nextSibling.get_text()
                    else:
                        td = soup.findAll('strong', string="分享率", limit=1)
                        if len(td) != 0:
                            ratio = td[0].nextSibling.nextSibling.get_text()
                        else:
                            td = soup.findAll('font', {'class':'color_ratio'}, limit=1)
                            ratio = td[0].nextSibling.get_text()
                        
                    data['ratio'] = ratio.strip()
                
                td = soup.findAll('td', string=["发布种子","發布種子"], limit=1)
                s = td[0].nextSibling.get_text()
                if '个种子' in s or '记录' in s:
                    #页面直接包含数据
                    if '察看' in s:
                        data['published_seed_num'] = s.split('，')[0].split('(')[-1].replace('个种子','')
                    else:
                        data['published_seed_num'] = re.sub(r'\D+', '', s)   
                else:
                    url = site_url + "/getusertorrentlistajax.php?userid=%s&type=uploaded" % data['user_id']
                    response = session.get(url, headers=headers, timeout=10)
                    soup1 = BeautifulSoup(response.text, "lxml")
                    published_seed_num= soup1.find('b')
                    if published_seed_num != None:
                        data['published_seed_num'] = published_seed_num.get_text()
                    else:
                        data['published_seed_num'] = 0
                        
                td = soup.findAll('td', string=["当前做种","目前做種"], limit=1)
                s = td[0].nextSibling.get_text()
                if '个种子' in s or '记录' in s:
                    if '察看' in s:
                        data['seed_num'] = s.split('，')[0].split('(')[-1].replace('个种子','')
                        data['totle_seed_size'] = s.split('，')[-1].replace(')','').replace('共计','')
                    else:
                        data['seed_num'] = re.sub(r'\D+', '', s)
                        data['totle_seed_size'] = 0
        
                else:
                    url = site_url +  "/getusertorrentlistajax.php?userid=%s&type=seeding" % data['user_id']
                    response = session.get(url, headers=headers, timeout=10)
                    soup1 = BeautifulSoup(response.text, "lxml")
                    seed_num= soup1.find('b')
                    if seed_num != None:
                        data['seed_num'] = seed_num.get_text()
                        data['totle_seed_size'] = seed_num.nextSibling.get_text().split('：')[-1]
                    else:
                        data['seed_num'] = 0
                        data['totle_seed_size'] = 0 
                return True, data                  
            else:
                data['msg'] = "格式错误"
                return False, data
                
        else:
            data['msg'] = "cookie过期"
            
            return False, data
            
    except:
        data['msg'] = "无法登录"
        
        return False, data    
