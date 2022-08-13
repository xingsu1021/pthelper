from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import NotifyConfig

# Create your views here.
class IyuuView(LoginRequiredMixin,TemplateView):
    """
    iyuu配置
    """
    template_name = 'notify/iyuu.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        得到
        """

        return super(IyuuView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):
        
        #获取iyuu记录
        iyuu_count = NotifyConfig.objects.filter(name='iyuu').count()
        if iyuu_count == 0:
            
            context = {}
        else:
            ormdata = NotifyConfig.objects.get(name='iyuu')
            context = {
                'id': ormdata.id,
                'name': ormdata.name,
                'iyuu_key': ormdata.iyuu_key,
            }
        kwargs.update(context)
        return super(IyuuView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        _id = request.POST.get('id','')
        iyuu_key = request.POST.get("iyuu_key").strip()
        
        iyuu_count = NotifyConfig.objects.filter(name='iyuu').count()
        if iyuu_count == 0:
            ormdata = NotifyConfig.objects.create(name='iyuu',
                                                  iyuu_key=iyuu_key,
                                                  )
        else:
            ormdata = NotifyConfig.objects.get(id=_id)
            ormdata.iyuu_key = iyuu_key

        ormdata.save()

        response_data={"code":1,"msg":"添加成功"}

        return JsonResponse(response_data)
    
#------------------------------
class TelegramView(LoginRequiredMixin,TemplateView):
    """
    Telegram配置
    """
    template_name = 'notify/telegram.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        得到
        """

        return super(TelegramView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):
        
        #获取记录
        telegram_count = NotifyConfig.objects.filter(name='telegram').count()
        if telegram_count == 0:
            
            context = {}
        else:
            ormdata = NotifyConfig.objects.get(name='telegram')
            context = {
                'id': ormdata.id,
                'name': ormdata.name,
                'tg_chat_id': ormdata.tg_chat_id,
                'tg_token': ormdata.tg_token,
            }
        kwargs.update(context)
        return super(TelegramView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        _id = request.POST.get('id','')
        tg_chat_id = request.POST.get("tg_chat_id").strip()
        tg_token = request.POST.get("tg_token").strip()
        
        telegram_count = NotifyConfig.objects.filter(name='telegram').count()
        if telegram_count == 0:
            ormdata = NotifyConfig.objects.create(name='telegram',
                                                  tg_chat_id=tg_chat_id,
                                                  tg_token=tg_token,
                                                  )
        else:
            ormdata = NotifyConfig.objects.get(id=_id)
            ormdata.tg_chat_id = tg_chat_id
            ormdata.tg_token = tg_token

        ormdata.save()

        response_data={"code":1,"msg":"添加成功"}

        return JsonResponse(response_data)
    
#------------------------------
class EmailView(LoginRequiredMixin,TemplateView):
    """
    Email配置
    """
    template_name = 'notify/email.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        得到
        """

        return super(EmailView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):
        
        #获取记录
        email_count = NotifyConfig.objects.filter(name='email').count()
        if email_count == 0:
            
            context = {}
        else:
            ormdata = NotifyConfig.objects.get(name='email')
            context = {
                'id': ormdata.id,
                'name': ormdata.name,
                'mail_type': ormdata.mail_type,
                'smtp_user': ormdata.smtp_user,
                'smtp_password': ormdata.smtp_password,
                'receive_user': ormdata.receive_user,
            }
        kwargs.update(context)
        return super(EmailView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        _id = request.POST.get('id','')
        mail_type = request.POST.get("mail_type").strip()
        smtp_user = request.POST.get("smtp_user").strip()
        smtp_password = request.POST.get("smtp_password").strip()
        receive_user = request.POST.get("receive_user","").strip()
        
        if receive_user == '':
            receive_user = smtp_user
            
        email_count = NotifyConfig.objects.filter(name='email').count()
        if email_count == 0:
            ormdata = NotifyConfig.objects.create(name='email',
                                                  mail_type=mail_type,
                                                  smtp_user=smtp_user,
                                                  smtp_password=smtp_password,
                                                  receive_user=receive_user,
                                                  )
        else:
            ormdata = NotifyConfig.objects.get(id=_id)
            ormdata.mail_type = mail_type
            ormdata.smtp_user = smtp_user
            ormdata.smtp_password = smtp_password
            ormdata.receive_user = receive_user

        ormdata.save()

        response_data={"code":1,"msg":"添加成功"}

        return JsonResponse(response_data)
    
#------------------------------
class EnWechatView(LoginRequiredMixin,TemplateView):
    """
    企业微信配置
    """
    template_name = 'notify/enwechat.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        得到
        """

        return super(EnWechatView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):
        
        #获取记录
        num = NotifyConfig.objects.filter(name='enwechat').count()
        if num == 0:
            
            context = {}
        else:
            ormdata = NotifyConfig.objects.get(name='enwechat')
            context = {
                'id': ormdata.id,
                'name': ormdata.name,
                'enwechat_corp_id': ormdata.enwechat_corp_id,
                'enwechat_agent_id': ormdata.enwechat_agent_id,
                'enwechat_agent_secret': ormdata.enwechat_agent_secret,
                'receive_user': ormdata.receive_user,
            }
        kwargs.update(context)
        return super(EnWechatView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        _id = request.POST.get('id','')
        enwechat_corp_id = request.POST.get("enwechat_corp_id").strip()
        enwechat_agent_id = request.POST.get("enwechat_agent_id").strip()
        enwechat_agent_secret = request.POST.get("enwechat_agent_secret").strip()
        receive_user = request.POST.get("receive_user","").strip()

            
        num = NotifyConfig.objects.filter(name='enwechat').count()
        if num == 0:
            ormdata = NotifyConfig.objects.create(name='enwechat',
                                                  enwechat_corp_id=enwechat_corp_id,
                                                  enwechat_agent_id=enwechat_agent_id,
                                                  enwechat_agent_secret=enwechat_agent_secret,
                                                  receive_user=receive_user,
                                                  )
        else:
            ormdata = NotifyConfig.objects.get(id=_id)
            ormdata.enwechat_corp_id = enwechat_corp_id
            ormdata.enwechat_agent_id = enwechat_agent_id
            ormdata.enwechat_agent_secret = enwechat_agent_secret
            ormdata.receive_user = receive_user

        ormdata.save()

        response_data={"code":1,"msg":"添加成功"}

        return JsonResponse(response_data)