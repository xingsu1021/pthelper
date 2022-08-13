#coding=utf-8
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import NotifyConfig,MailType

import requests
import datetime
from urllib import parse
import simplejson as json
import telegram
import sys
from common.utils import send_email, EnWechat

#直接使用检查是否管理员
#from django.contrib.auth.decorators import user_passes_test
#@user_passes_test(lambda u: u.is_superuser)

@login_required
def iyuutest(request):
    """        
    提供相应的数据
    """

    _id = request.POST.get('id','')

    if _id == '':
        
        response_data={"code":0,"msg":"请先配置IYUU令牌"}

    else:
        
        ormdata = NotifyConfig.objects.get(id=_id)
        iyuu_key = ormdata.iyuu_key
        
        
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        headers = {
            'user_agent': user_agent,
            'Content-type': 'application/x-www-form-urlencoded'
        }
        
        now_time = parse.quote('<center><b><font color="#55a7e3">') + parse.unquote(time) + parse.quote('</font></b></center><br>')
        send_txts = parse.quote('<center><b><font color="#4CAF50">[测试]</font></b></center><br>')
        api = 'https://iyuu.cn/' + iyuu_key + '.send'
        sen_url = api + '?text='+ parse.quote('测试提示') + '&desp=' + now_time + send_txts
        response = requests.get(sen_url, headers=headers ,verify=False)

        response_msg = json.loads(response.text)
        if response.status_code == 200 and response_msg['errcode'] == 0:
            response_data={"code":1,"msg":"发送测试成功"}
        else:
            response_data={"code":0,"msg":"发送测试失败,%s" % response_msg['errmsg'] }

    return JsonResponse(response_data)

@login_required
def telegramtest(request):
    """        
    提供相应的数据
    """

    _id = request.POST.get('id','')

    if _id == '':
        
        response_data={"code":0,"msg":"请先配置Telegram"}

    else:
        
        ormdata = NotifyConfig.objects.get(id=_id)
        tg_chat_id = ormdata.tg_chat_id
        tg_token = ormdata.tg_token
        
        bot = telegram.Bot(token = tg_token)
        
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            
            response = bot.send_message(chat_id=tg_chat_id,
                text='<b>%s</b><i><b>[测试]</b></i>' % time,
                parse_mode=telegram.ParseMode.HTML)
        
            #response_msg = json.loads(response)
            response_data={"code":1,"msg":"发送测试成功"}
        except:
            ex_type, ex_val, ex_stack = sys.exc_info()

            if 'Chat not found' in str(ex_val):
                response_data={"code":0,"msg":"发送测试失败,未找到频道ID" }
            elif 'Unauthorized' in str(ex_val):
                response_data={"code":0,"msg":"发送测试失败,令牌配置错误" }
            else:
                response_data={"code":0,"msg":"发送测试失败,请联系管理员" }

    return JsonResponse(response_data)

@login_required
def emailtest(request):
    """        
    提供相应的数据
    """

    _id = request.POST.get('id','')

    if _id == '':
        
        response_data={"code":0,"msg":"请先配置邮箱"}

    else:
        
        ormdata = NotifyConfig.objects.get(id=_id)
        mail_type = ormdata.mail_type
        smtp_user = ormdata.smtp_user
        smtp_password = ormdata.smtp_password
        receive_user = ormdata.receive_user
        
        receiver_users = []
        for i in receive_user.split(","):
            receiver_users.append(i)

        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            
            sendata='<font color="#4CAF50"><b>%s</b><i><b>[测试]</b></i></font>' % time
            
            flag,response = send_email(mail_type,smtp_user,smtp_password,receiver_users,sendata,isTest=True)

            #response_msg = json.loads(response)
            response_data={"code":1,"msg":response}
        except Exception as e:
            response_data={"code":0,"msg":str(e) }

    return JsonResponse(response_data)

@login_required
def enwechattest(request):
    """        
    提供相应的数据
    """

    _id = request.POST.get('id','')

    if _id == '':
        
        response_data={"code":0,"msg":"请先配置企业微信"}

    else:
        
        ormdata = NotifyConfig.objects.get(id=_id)
        enwechat_corp_id = ormdata.enwechat_corp_id
        enwechat_agent_id = ormdata.enwechat_agent_id
        enwechat_agent_secret = ormdata.enwechat_agent_secret
        receive_user = ormdata.receive_user
        
        receiver_users = []
        for i in receive_user.split(","):
            receiver_users.append(i)

        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            weclient = EnWechat(corp_id=enwechat_corp_id, agent_id=enwechat_agent_id, agent_secret=enwechat_agent_secret)
                        
            sendata="""<font color="#4CAF50">%s [测试]</font>""" % time
            
            flag,response = weclient.send_markdown(receiver_users,sendata)

            #response_msg = json.loads(response)
            response_data={"code":1,"msg":response}
        except Exception as e:
            response_data={"code":0,"msg":str(e) }

    return JsonResponse(response_data)

#==================
@login_required
def mailtypeinfo(request):
    """ 
    邮箱类型
    xmSelect
    """

    data = {}
    data['code'] = 0
    data['msg'] = ""
    data['data'] = []

    #得到排序字段
    sort = request.GET.get('sort','name')
    #得到排序规则
    order_by_type = request.GET.get('order','desc')
    
    if order_by_type == 'desc':
        order_by = sort
    else:
        order_by = '-' + sort
        
    #获取所有记录
    data['count'] = MailType.objects.count()

    ormdata = MailType.objects.order_by(order_by).all()

    for i in ormdata:

        data['data'].append({
                         "name":i.name,
                         "value":i.alias_name
                         })

    return JsonResponse(data)