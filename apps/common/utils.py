# -*- coding: utf-8 -*-
#
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.encoding import filepath_to_uri
from collections import OrderedDict
import os
import sys
import logging
import datetime
import time
import hashlib
from email.utils import formatdate
import calendar
import threading
import uuid
import requests 
import simplejson as json
import ftplib
import socket
from urllib.parse import urlparse
import pytz
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import telegram
from urllib import parse
from wechatpy.enterprise import WeChatClient
from PIL import Image, ImageDraw, ImageFont
import re

logger = logging.getLogger('django')

def download_file(url, fname):
    """
    下载文件
    """

    download_path = os.path.join(settings.BASE_DIR, 'downloads')

    if not os.path.exists(download_path):
        os.makedirs(download_path)
        
    download_file = os.path.join(download_path, fname)
        
    data = requests.get(url, stream=True)
    try:
        data.raise_for_status()
        
        with open(download_file, "wb") as updatefile:
            for chunk in data.iter_content(chunk_size=1024):
                if chunk:
                    updatefile.write(chunk)
        return True, download_file
    except Exception as exc:
        print('There was a problem: %s' % (exc))
        return False, None

def check_filename(name, extname = ['rpm','tar','tar.gz','gz'], is_url=True):
    """
    检查文件是否是需要的扩展名
    返回： True/False, 文件名
    """
    if is_url:
        #解析url
        parse_url = urlparse(name)
        url_path=parse_url.path
        pkg_name = (os.path.basename(url_path))
        #file_name, extension_name = os.path.splitext(pkg_name)
        extension_name = os.path.splitext(pkg_name)[-1][1:]
    else:
        pkg_name = (os.path.basename(name))
        extension_name = os.path.splitext(pkg_name)[-1][1:]

    if extension_name in extname:
        return True, pkg_name
    else:
        return False, pkg_name
    

def get_logger(name=None):
    return logging.getLogger('%s' % name)

def get_clientip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        clientip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        clientip = request.META['REMOTE_ADDR']

    return {'clientip': clientip, 'user': request.user}
      

def timesince(dt, since='', default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days, 5 hours.
    """

    if since == '':
        since = datetime.datetime.utcnow()

    if since == None:
        return default

    diff = since - dt

    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        if period:
            return "%d %s" % (period, singular if period == 1 else plural)
    return default

_STRPTIME_LOCK = threading.Lock()


def now_date():
    """当前时间"""
    return datetime.datetime.now()

def date_to_unixtime(datetime):
    """将datetime转换成unixtime"""
    return time.mktime(datetime.timetuple())

def to_unixtime_old(time_string, format_string):
    time_string = time_string.decode("ascii")
    with _STRPTIME_LOCK:
        return int(calendar.timegm(time.strptime(time_string, format_string)))

def to_unixtime(time_string, format_string):
    """
    时间字符串转成unix时间戳
    """
    return int(calendar.timegm(time.strptime(time_string, format_string)))

def http_date(timeval=None):
    """返回符合HTTP标准的GMT时间字符串，用strftime的格式表示就是"%a, %d %b %Y %H:%M:%S GMT"。
    但不能使用strftime，因为strftime的结果是和locale相关的。
    """
    return formatdate(timeval, usegmt=True)


def http_to_unixtime(time_string):
    """把HTTP Date格式的字符串转换为UNIX时间（自1970年1月1日UTC零点的秒数）。

    HTTP Date形如 `Sat, 05 Dec 2015 11:10:29 GMT` 。
    """
    _GMT_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
    return to_unixtime(time_string, _GMT_FORMAT)

def cst_to_unixtime(time_string):
    """
    2018-10-17 12:39:30 CST+0800
    """
    _CST_FORMAT = "%Y-%m-%d %H:%M:%S CST%z"
    return to_unixtime(time_string, _CST_FORMAT)

def iso8601_to_unixtime(time_string):
    """把ISO8601时间字符串（形如，2012-02-24T06:07:48.000Z）转换为UNIX时间，精确到秒。"""
    _ISO8601_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"
    return to_unixtime(time_string, _ISO8601_FORMAT)

def str2datetime(st, s_format='%Y-%m-%d %H:%M:%S'):
    """字符串转成datetime
    CST_FORMAT = "%Y-%m-%d %H:%M:%S CST%z"
    """
    return datetime.datetime.strptime(st, s_format)

def str2utcdatetime(st,from_format='%Y-%m-%d %H:%M:%S', utc_format='%Y-%m-%dT%H:%M:%SZ',tz=True):
    """字符串时间转UTC时间（-8:00)"""
    local_st = datetime.datetime.strptime(st, from_format)
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    if tz:
        return utc_st.strftime(utc_format)
    else:
        return utc_st

def datetime2utc(local_st):
    """本地时间转UTC时间（-8:00)"""
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st

def utc2datetime(utc_st):
    """UTC时间转本地时间（+8:00）"""
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st

def utc_to_local_unixtime(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%SZ'):
    """
    utc字符转转换成unix时间戳
    '2019-01-16T11:30:00Z'
    '2019-01-16 11:30:00+00:00', utc_format='%Y-%m-%d %H:%M:%S+00:00'
    """
    local_tz = pytz.timezone('Asia/Shanghai')
    local_format = "%Y-%m-%d %H:%M:%S"
    utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    return int(time.mktime(time.strptime(time_str, local_format)))

def capacity_convert(size, expect='auto', rate=1000):
    """
    :param size: '100MB', '1G'
    :param expect: 'K, M, G, T
    :param rate: Default 1000, may be 1024
    :return:
    """
    rate_mapping = (
        ('K', rate),
        ('KB', rate),
        ('M', rate**2),
        ('MB', rate**2),
        ('G', rate**3),
        ('GB', rate**3),
        ('T', rate**4),
        ('TB', rate**4),
    )

    rate_mapping = OrderedDict(rate_mapping)

    std_size = 0  # To KB
    for unit in rate_mapping:
        if size.endswith(unit):
            try:
                std_size = float(size.strip(unit).strip()) * rate_mapping[unit]
            except ValueError:
                pass

    if expect == 'auto':
        for unit, rate_ in rate_mapping.items():
            if rate > std_size/rate_ > 1:
                expect = unit
                break
    expect_size = std_size / rate_mapping[expect]
    return expect_size, expect

def filesizeformat(value, baseMB=False):
    """将字节转换为 1.00KB 1.00Mb 1.00gb
    """
    try:
        bytes = float(value)
    except:
        return 0

    if baseMB is True:
        bytes = bytes * 1024 * 1024

    base = 1024

    if bytes == 0:
        return '0'

    ret = '0'
    if bytes < base:
        ret = '%d Bytes' % (bytes)
    elif bytes < base * base:
        ret = '%.2f KB' % (bytes / base)
    elif bytes < base * base * base:
        ret = '%.2f MB' % (bytes / (base * base))
    elif bytes < base * base * base * base:
        if bytes % (base * base * base) >= 0:
            ret = '%.2f GB' % (bytes / (base * base * base))
        else:
            ret = "%.2f MB" % (bytes / (base * base))
    else:
        ret = '%.2f TB' % (bytes / (base * base * base * base))

    return ret

def sum_capacity(cap_list):
    total = 0
    for cap in cap_list:
        size, _ = capacity_convert(cap, expect='K')
        total += size
    total = '{} K'.format(total)
    return capacity_convert(total, expect='auto')


def str_to_md5(strs):  
    m=hashlib.md5()  
    m.update(strs.encode("utf8"))  
    return m.hexdigest()

def int_random():
    """使用uuid生产随机数,返回128位整数"""
    u = uuid.uuid1()
    return u.int

def hex_random():
    """使用uuid生产随机数,返回32位十六进制"""
    u = uuid.uuid1()
    return u.hex
 
def iso8601_to_time(time_string):
    """把ISO8601时间字符串（形如，2012-02-24T06:07:48.000Z）转换为UNIX时间，精确到秒。"""
    return time_string.strftime('%Y-%m-%d %H:%M:%S')

def str_to_datetime(string):
    """字符串 2017-10-21 00:00:00 格式化为datetime"""
    return datetime.datetime.strptime(string,"%Y-%m-%d %H:%M:%S")


def sumplus(*args):
    """求和"""
    r = 0.0
    for n in args:
        r += float(n)
    return "%.2f" % r

def sumplusInt(*args):
    """求和"""
    r = 0
    for n in args:
        r += int(n)
    return r

class ImageStorage(FileSystemStorage): 
    """
    图片上传
    """ 
    
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):  
        #初始化  
        super(ImageStorage, self).__init__(location, base_url)  
  
    #重写 _save方法          
    def _save(self, name, content):  
        
        #文件扩展名  
        ext = os.path.splitext(name)[1]  
        #文件目录  
        d = os.path.dirname(name)  
        #定义文件名，年月日时分秒随机数
        year = time.strftime('%Y')
        month = time.strftime('%m')
        fn = time.strftime('%Y%m%d%H%M%S')  
        fn = fn + str(hex_random())
        #重写合成文件名  
        name = os.path.join('images', year,month, d, fn + ext)  
        #调用父类方法  
        return super(ImageStorage, self)._save(name, content)
       
def htmlfilesave(name, content, gameid):  
    """
    保存文件,返回url地址
    """
    
    #文件扩展名  
    ext = os.path.splitext(name)[1]  
 
    #定义文件名，年月日时分秒随机数
    year = time.strftime('%Y')
    month = time.strftime('%m')
    fn = time.strftime('%Y%m%d%H%M%S')  
    fn = fn + str(hex_random())
    #重写合成文件名  
    name = os.path.join('html', year,month, gameid, fn + ext) 
    #完整的文件路径 
    full_name = os.path.join(settings.MEDIA_ROOT, name)
    #得到url
    url = filepath_to_uri(os.path.join(settings.MEDIA_URL, name))

    directory = os.path.dirname(full_name)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except FileNotFoundError:
            pass

    if not os.path.isdir(directory):
        raise IOError("%s exists and is not a directory." % directory)

    #写入文件
    #open(full_name,'w', encoding='utf8').writelines(content.replace(settings.HTML_HREF_REPLACE_KEY, app_url))
    open(full_name,'w', encoding='utf8').writelines(content)

    return url

def writefile(content, apk_url, ext='html'):  
    """
    写文件，返回文件路径
    """
    ext = '.' + ext

    fn = time.strftime('%Y%m%d%H%M%S')  
    fn = fn + str(hex_random())
    #重写合成文件名  
    name = os.path.join('cdnfile', fn + ext) 
    #完整的文件路径 
    full_name = os.path.join(settings.MEDIA_ROOT, name)

    directory = os.path.dirname(full_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    #写入文件
    open(full_name,'w', encoding='utf8').writelines(content.replace(settings.HTML_HREF_REPLACE_KEY, apk_url))

    return full_name

def ftpupload(host, port, username, password, upload_dir, upload_file, rmfile=False):
    """上传文件到ftp"""
    
    timeout = 10
    ftp = ftplib.FTP()
    filename = os.path.basename(upload_file)
    try:
        #连接ftp
        ftp.connect(host=host, port=port, timeout=timeout)
    except (socket.error, socket.gaierror):
        return  False, "连接FTP失败 %s" % host
  
    try:
        #登录
        ftp.login(username, password)
    except ftplib.error_perm:
        return  False, "ftp用户名或密码错误"
    
    try:
        #切换到操作目录
        ftp.cwd(upload_dir)
    except:
        #切换目录失败,目录不存在
        #创建目录
        ftp.mkd(upload_dir)
        #切换目录
        ftp.cwd(upload_dir)
    
    fd=open(upload_file,'rb')
    #上传文件
    ftp.storbinary('STOR %s' % filename, fd)
    
    fd.close()
    ftp.quit()  

    #删除文件
    if rmfile:
        os.remove(upload_file)

    #返回写入的ftp地址
    url = filepath_to_uri(os.path.join('/', upload_dir, filename))

    return True,url 


class ExcelStorage(FileSystemStorage): 
    """
    excel文件上传
    """ 
    
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):  
        #初始化  
        super(ExcelStorage, self).__init__(location, base_url)  
  
    #重写 _save方法          
    def _save(self, name, content):  
        
        #文件扩展名  
        ext = os.path.splitext(name)[1]  
        #文件目录  
        d = os.path.dirname(name)  
        #定义文件名，年月日时分秒随机数
        year = time.strftime('%Y')
        month = time.strftime('%m')
        fn = time.strftime('%Y%m%d%H%M%S')  
        #fn = fn + str(hex_random())
        #重写合成文件名  
        name = os.path.join('excel', year,month, d, fn + ext)  
        #调用父类方法  
        return super(ExcelStorage, self)._save(name, content)

def send_email(mail_type,smtp_user,smtp_password,receiver_users = [],send_data = [] ,isTest=False, title='PT助手提示'):
    """
    发送邮件
    """
    
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    if isTest:
        content = "<h1>测试</h1>"
    else:
        content = '''
        <!DOCTYPE HTML>
        <html>
        <head>
        <meta charset="utf-8" />
        <style>
            .p1{text-indent: 40px;}
            .p2{text-indent: 2em;}
        </style>
        </head>
        <body>
            <p class="p2">%s</p>
            %s
        </body>
        </html>
        ''' % (time,"<br>".join(send_data))
        
        
    #title = "PT助手"
    #receiver = ["249545020@qq.com"]
    receiver = receiver_users
    msg = ''
    msg = MIMEText(content, 'html', 'utf-8')
    # 设置发送人
    msg['From'] = Header(smtp_user)
    # 设置接收人
    msg['To'] = Header(str(";".join(receiver)))
    # 设置邮件标题
    msg['Subject'] = Header(title)
    
    try:
        if mail_type == "qq":
            smtp_client = smtplib.SMTP_SSL("smtp.qq.com", 465)
        elif mail_type == "163":
            smtp_client = smtplib.SMTP_SSL("smtp.163.com", 465)
        elif mail_type == "sina":
            try:
                #sina不支持sslv3
                smtp_client = smtplib.SMTP_SSL("smtp.sina.com", 465)
            except:
                #sslv3失败后使用明文
                smtp_client = smtplib.SMTP("smtp.sina.com", 25)
        else:
            return False,"未知邮件类型"
        
        smtp_client.login(smtp_user, smtp_password)
        smtp_client.sendmail(smtp_user, receiver, msg.as_string())
        smtp_client.quit()
        
    except smtplib.SMTPException as e:
        logging.error(str(e))
        return False,str(e)
    
    return True,"发送成功"

def send_telegram(tg_chat_id,tg_token,send_data = [] ,isTest=False, title='PT助手提示'):
    

    bot = telegram.Bot(token = tg_token)
    
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        if isTest:
            bot.send_message(chat_id=tg_chat_id,
                text='<b>%s</b><i><b>[测试]</b></i>' % time,
                parse_mode=telegram.ParseMode.HTML)
        else:
            bot.send_message(chat_id=tg_chat_id,
                text='<b>%s</b><i><b>\r\n%s</b></i>' % (time,"\r\n".join(send_data).replace('font','a')),
                parse_mode=telegram.ParseMode.HTML)
    
    except:
        ex_type, ex_val, ex_stack = sys.exc_info()
    
        logging.error(str(ex_val))
                      
        if 'Chat not found' in str(ex_val):
            msg = "发送测试失败,未找到频道ID"
        elif 'Unauthorized' in str(ex_val):
            msg = "发送测试失败,令牌配置错误" 
        else:
            msg = "发送测试失败,请联系管理员"
        return False, msg
            
    return True,"发送成功"

def send_iyuu(iyuu_key,send_data = [] ,isTest=False, title='PT助手提示'):
    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    
    #针对不同通知类型进行处理
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    headers = {
        'user_agent': user_agent,
        'Content-type': 'application/x-www-form-urlencoded'
    }
    now_time = parse.quote('<center><b><font color="#55a7e3">') + parse.unquote(time) + parse.quote('</font></b></center><br>')
    api = 'https://iyuu.cn/' + iyuu_key + '.send'
    if isTest:
        send_txts = parse.quote('<center><b><font color="#4CAF50">[测试]</font></b></center><br>')
        sen_url = api + '?text='+ parse.quote('测试提示') + '&desp=' + now_time + send_txts
    else:
        send_txts = parse.quote('<br>'.join(send_data))
        sen_url = api + '?text='+ parse.quote(title) + '&desp=' + now_time + send_txts
        
    try:
        response = requests.get(sen_url, headers=headers ,verify=False)
        response_msg = json.loads(response.text)
        if response.status_code == 200 and response_msg['errcode'] == 0:
            msg = "发送成功"
        else:
            msg = "发送测试失败,%s" % response_msg['errmsg']
            return False, msg
    except:
        logging.error("连接IYUU失败")
        return False, "连接IYUU失败"
        
    return True,"发送成功"

def send_enwechat(corp_id = None, agent_id = None, agent_secret = None, user_ids = [], send_data = [] ,isTest=False, title='PT助手提示'):
    """发送企业微信消息"""
    
    weclient = EnWechat(corp_id=corp_id, agent_id=agent_id, agent_secret=agent_secret)
    
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    if isTest:
        #发送测试消息
        text = '<div class="highlight">测试 %s</div>'  % time
        flag, response = weclient.send_text(user_ids, text)
        if flag:
            msg = "发送成功"
            return True, msg
        else:
            msg = response["errmsg"]
            return False, msg
        
    else:
        #生成图片
        image_file_path = create_image(send_data)
        #上传图片
        flag, response = weclient.upload_image(image_file_path)
        if flag:
            #发送文本卡片
            flag, response = weclient.send_text_card(user_ids, response)
            if flag:
                return True, "发送成功"
            else:
                return False, response
        else:
            return False, response
            
        
def getSiteUrl(url):
    """
    获取官网url
    """
    u = urlparse(url)
    site_url = u.scheme + "://" + u.netloc
    
    return site_url

def parseUrl(url):
    """
    拆解url
    #scheme='https', netloc='127.0.0.1:8080', path='/', params='', query='', fragment=''
    """
    data = {}
    u = urlparse(url)

    # http,https
    data['protocol'] = u.scheme
    data['url'] = u.netloc
    data['host'] = u.netloc.split(":")[0]
    data['port'] = u.port
    data['path'] = u.path
    data['params'] = u.params
    data['query'] = u.query
    
    return data

def create_image(msg_content = []):
    """
    图片生成
    msg 生成图片的文字
    """
    
    #f = open("e:/test/test.txt","r",encoding='utf-8').readlines()
     
    if sys.platform == "win32":
        # 设置字体及字号,加载宋体,否则中文乱码
        font = ImageFont.truetype("simsun.ttc", 20, encoding="unic") 
    else:
        #linux加载目录下字体
        font = ImageFont.truetype(os.path.join(settings.BASE_DIR, "fonts", "simsun.ttc"), 20, encoding="unic") 
        
    #图片宽度
    image_width = 500
    #图片高度,可以通过font.getbbox(line)[3]获取字体高度 21
    image_high = len(msg_content) * 25
    
    # 设置画布大小及背景色(白色)
    image = Image.new('RGB', (image_width, image_high), (255,255,255))     
    
    draw = ImageDraw.Draw(image)
    
    x = 10
    y = 5
    
    for line in msg_content:
        #print(line)
        if '成功' in line:
            fill='green'
        else:
            fill='red'
        #替换掉<>间的内容
        line = re.sub(re.compile('<.*?>') , '', line)
        #通过x,y坐标循环写入
        draw.text((x, y), line, font=font, fill=fill)
        #print (font.getbbox(line))
        #获取行的字体高度
        y += font.getbbox(line)[3]
    
    del draw 
    
    image_file_name = os.path.join(settings.TMP_LOG_DIR, "msg.png")
    image.save(image_file_name,"PNG") # 保存图片
    
    return image_file_name


def cookie_parse(cookie_str):
    cookie_dict = {}
    cookies = cookie_str.split(";")
    for cookie in cookies:
        cookie = cookie.split("=")
        cookie_dict[cookie[0]] = cookie[1]
    return cookie_dict

class EnWechat:
    def __init__(self, corp_id=None, agent_id=None, agent_secret=None):
        """企业微信"""
        self.corp_id = corp_id
        self.agent_id = agent_id
        self.agent_secret = agent_secret
        self.client = self.weclient()
        
    def weclient(self):
        return WeChatClient(self.corp_id, self.agent_secret)
        
    def getDepartmentUsers(self, department_id = None):
        """获取部门下的所有用户ID
        #返回：{姓名: 用户ID}
        """
        try:
            
            return True, self.client.department.get_map_users(id = department_id)
            
        except Exception as e:
            return False, str(e) 
        
    def getDepartmentUsersID(self, department_id = None):
        """获取部门下的所有用户ID
        
        """
        try:
            #返回：{姓名: 用户ID}
            user_ids = self.client.department.get_map_users(id = department_id)
            return list(user_ids.values())
        except Exception as e:
            return False, str(e)
            
    def send_text(self, user_ids = [], msg = None):
        """发送文本消息
        返回
        {'errcode': 0, 'errmsg': 'ok', 'msgid': 'fcLc6UhB2absSaoEDgOVFJc7rUS6HAUpkVR6y2ltzLhzzjUH_WfDNW5dVl7nScRT2AG7lQ475r8M9qyISlX9BQ'}
        """
        r = self.client.message.send_text(self.agent_id, user_ids, msg)
        if r['errcode'] == 0:
            return True, r['msgid']
        else:
            return True, r['errmsg']

        
    def send_markdown(self, user_ids = [], msg = None):
        """发送markdown消息
        https://developer.work.weixin.qq.com/document/path/90236#%E6%94%AF%E6%8C%81%E7%9A%84markdown%E8%AF%AD%E6%B3%95
        """
        return True, self.client.message.send_markdown(self.agent_id, user_ids, msg)
        #try:
            #return True, self.client.message.send_markdown(self.agent_id, user_ids, msg)
        #except Exception as e:
            #return False, str(e)
            
    def send_image(self, user_ids = [], media_id = None):
        """发送图片消息
        """
        
        return True, self.client.message.send_image(self.agent_id, user_ids, media_id)
    
    def send_text_card(self, user_ids = [], url = None):
        """发送文本卡片消息
        url为上传微信的素材地址
        """
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        description = '<div class="gray">' + time + '</div>'
        title = '签到通知'
        
        return True, self.client.message.send_text_card(self.agent_id, user_ids, title, description, url)
    
    def upload_image(self, image_file_path = None):
        """
        上传图片素材(永久,url限制微信使用)
        image_file_path 要上传的本地图片路径
        
        返回 url地址
        {'errcode': 0, 'errmsg': 'ok', 'url': 'https://wework.qpic.cn/wwpic/592170_HhXMIUytR62CdSy_1662426978/0'}
        """
        
        with open(image_file_path, 'rb') as f:
            image = f.read()        
        #上传图片
        reponse = self.client.media.upload_img(image)

        if reponse['errcode'] == 0:
            url = reponse['url']
            
            return True, url
        else:
            msg = reponse['errmsg']
            
            return False, msg
            
    def upload(self, media_type = "image", media_file = None):
        """
        上传临时素材(保留3天)
        media_type 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        media_file – 要上传的文件，一个 File-object
        
        返回 media_id
        {"errcode": 0, "errmsg": "ok", "type": "image", "media_id": "3Y7qMZUYZvhZG13oNoKMKMWaxtNupLKIR4lgUsDc0abqicTjGnuE9APt-NiivZ3tg", "created_at": "1662427932"}
        """
        
        with open(media_file, 'rb') as f:
            file_content = f.read()
            
        #上传
        reponse = self.client.media.upload(media_type, file_content)
        
        if reponse['errcode'] == 0:
            media_id = reponse['media_id']
            
            return True, media_id
        else:
            msg = reponse['errmsg']
            
            return False, msg        