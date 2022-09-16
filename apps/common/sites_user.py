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
            
            tables = soup.findAll('table', {'id':'info_block'})
            #print(tables)
            if len(tables) != 0:
                
                #span获取有2个，一个为用户信息，一个为信箱信息
                info = tables[0].findAll('span', {'class':'medium'})
                if info == []:
                    #获取只有1个
                    info = tables[0].findAll('span', {'class':'nowrap'})
                    user_info = info[0]
                else:
                    user_info = info[0]
                
                #print(user_info)
                #print("-------------")
                #用户详情链接
                user_info_link = user_info.a.attrs['href']
                #获取用户ID
                user_id = parseUrl(user_info_link)['query'].get('id',[])[0]
                #用户名
                user_name = user_info.a.get_text()
                #个人页无分享率的情况
                try:
                    #分享率
                    ratio = user_info.find('font',{'class':'color_ratio'}).nextSibling.get_text()
                    data['ratio'] = ratio
                except:
                    data['ratio'] = '0'
                    
                #print("user_info_link--->",user_info_link)
                #print("user_id--->",user_id)
                #print("user_name--->",user_name)
                data['user_id'] = user_id
                data['user_name'] = user_name
                if user_id == []:
                    data['msg'] = "格式错误"
                    return False, data
                    
                userdetails_url = site_url + "/userdetails.php?id=%s" % user_id
        
                response = session.get(userdetails_url, headers=headers, timeout=10)
                
                soup = BeautifulSoup(response.text, "lxml")
                
                tables = soup.findAll('table', {'class':'main'}, limit=2)
                if len(tables) == 2:
                    user_table = tables[1]#.find('table')
                else:
                    user_table = []
             
                if user_table != []:
                    #print(user_table)
                    
                    for index, tr in enumerate(user_table.find_all('tr')):
                            
                        if index == 0:
                            continue
            
                        #由于获取td后 标题内存在一个table,实际完整的一个是15个td，标题后面2个td废弃
                        tds = tr.find_all('td')
                        #print(tds)
                        #if '用户ID' in tds[0].get_text():
                            #data['user_id'] = tds[1].get_text()
                        data_key = tds[0].get_text().strip()
                        data_value = tds[1].get_text().strip()                        
                        #if ('邀请' in tds[0].get_text() and '邀请人' not in tds[0].get_text()) or ('邀請' in tds[0].get_text() and '邀請人' not in tds[0].get_text()):
                            #if RepresentsInt(tds[1].get_text()):
                                #data['invite'] = tds[1].get_text()
                            #else:
                                #data['invite'] = 0
                        if '邀请' == data_key or '邀請' == data_key or '剩余邀请量' == data_key :
                            #print(data_value)
                            #删除非数字字符(获取字符串的整数) \D：表示非数字
                            num = re.sub(r'\D+', '', data_value)
                            if RepresentsInt(num):
                                data['invite'] = num
                            else:
                                data['invite'] = 0                            
                            
                            #data['invite'] = data_value
                            
                        #if '加入日期' in tds[0].get_text():
                            ##替换括号和括号的内容为空
                            #data['create_time'] = re.sub("\(.*\)",'',tds[1].get_text())
                        if '加入日期' == data_key:
                            data['create_time'] = re.sub("\(.*\)",'', data_value)
                            
                        if '分享率' in tds[0].get_text():
                            data['ratio'] = tds[0].font.get_text()
                            
                        if ('上传量' in tds[0].get_text() and '实际' not in tds[0].get_text()) or ('上傳量' in tds[0].get_text() and '實際' not in tds[0].get_text()):
                            data['upload'] = re.sub("\(.*\)",'',tds[0].get_text().split(':')[-1])
                            data['download'] = re.sub("\(.*\)",'',tds[1].get_text().split(':')[-1])
                            
                        #pttime
                        if '核心数据' == data_key:
                            data['ratio'] = tds[1].font.get_text()
                            #分隔4个连续空格['', '上传量:  21.367TB\n            ', '下载量:  5.072TB', '魔力值:  6469.8']
                            d =tds[1].font.nextSibling.get_text().split(u'\xa0\xa0\xa0\xa0')
                            data['upload'] = d[1].split(':')[-1].replace('\\n','').strip()
                            data['download'] = d[2].split(':')[-1].strip()
                            data['bonus'] = d[3].split(':')[-1].strip()
                            
                        if '等级' in tds[0].get_text() or '等級' in tds[0].get_text():
                            data['level'] = re.sub("\(.*\)",'',tds[1].img.attrs['title'])
            
                        #if '魔力值' in tds[0].get_text():
                            #data['bonus'] = tds[1].get_text()
                            
                        if '魔力值' == data_key:
                            data['bonus'] = data_value
                            
                        if '做种积分' in tds[0].get_text():
                            data['score'] = tds[1].get_text()
                            
                        if '发布种子' in tds[0].get_text() or '發布種子' in tds[0].get_text():
                            if '个种子' in tds[1].get_text():
                                #页面直接包含数据
                                data['published_seed_num'] = tds[1].a.nextSibling.get_text().split('，')[0].replace('(','').replace('个种子','')
                            else:
                                url = getSiteUrl(site_url) + "/getusertorrentlistajax.php?userid=%s&type=uploaded" % data['user_id']
                                response = session.get(url, headers=headers, timeout=10)
                                soup = BeautifulSoup(response.text, "lxml")
                                published_seed_num= soup.find('b')
                                if published_seed_num != None:
                                    data['published_seed_num'] = published_seed_num.get_text()
                                else:
                                    data['published_seed_num'] = 0
                                
                        if '当前做种' in tds[0].get_text() or '目前做種' in tds[0].get_text():
                            if '个种子' in tds[1].get_text():
                                data['seed_num'] = tds[1].a.nextSibling.get_text().split('，')[0].replace('(','').replace('个种子','')
                                data['totle_seed_size'] = tds[1].a.nextSibling.get_text().split('，')[-1].replace('(','').replace('共计','')
                            else:
                                url = getSiteUrl(site_url) +  "/getusertorrentlistajax.php?userid=%s&type=seeding" % data['user_id']
                                response = session.get(url, headers=headers, timeout=10)
                                soup = BeautifulSoup(response.text, "lxml")
                                seed_num= soup.find('b')
                                if seed_num != None:
                                    data['seed_num'] = seed_num.get_text()
                                    data['totle_seed_size'] = seed_num.nextSibling.get_text().split('：')[-1]
                                    #pttime
                                    if '记录' in data['totle_seed_size']:
                                        url = site_url +  "/getusertorrentlist.php?userid=%s&type=seeding" % data['user_id']
                                        response = session.get(url, headers=headers, timeout=10)
                                        soup = BeautifulSoup(response.text, "lxml")
                                        tds = soup.findAll('td',{'id':'outer'}, limit=2)
                                        #print(tds)
                                        span = tds[1].find_all('span')
                                        #print(span[1].get_text())
                                        data['totle_seed_size'] = span[2].get_text().split('：')[-1].replace(u'\xa0','')                                    
                                else:
                                    data['seed_num'] = 0
                                    data['totle_seed_size'] = 0
                    return True, data
                else:
                    data['msg'] = "格式错误"
                    return False, data                    
            else:
                data['msg'] = "格式错误"
                return False, data
                
        else:
            data['msg'] = "cookie过期"
            
            return False, data
            
    except:
        data['msg'] = "无法登录"
        
        return False, data    
