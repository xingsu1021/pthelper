from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db import transaction
import uuid

from .models import Config, Rule, SeedInfo
from sites.models import SiteInfo
from download.models import Tools
from cron.crontabs import my_scheduler
from notify.models import NotifyConfig
from cron.models import Job

# Create your views here.

class RssConfigListView(LoginRequiredMixin,TemplateView):
    """
    显示
    """
    template_name = 'rss/rssconfig.html'

    def get(self, request, *args, **kwargs):
        """
        
        """
        return super(RssConfigListView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            # 'data': self.ormdata_game
        }
        kwargs.update(context)
        return super(RssConfigListView, self).get_context_data(**kwargs)
    
    
class RssConfigAddView(LoginRequiredMixin,TemplateView):
    """
    添加
    """
    template_name = 'rss/rssconfigadd.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        """
        return super(RssConfigAddView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
        }
        kwargs.update(context)
        return super(RssConfigAddView, self).get_context_data(**kwargs)


    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        siteinfo_id = request.POST.get("siteinfo_id").strip()
        url = request.POST.get("url").strip()

        ormdata_siteinfo = SiteInfo.objects.get(id=int(siteinfo_id))
        
        ormdata = Config.objects.create(url=url,
                                        siteinfo_id=ormdata_siteinfo
                                        )

        ormdata.save()
        
        response_data={"code":1,"msg":"添加成功"}
        

        return JsonResponse(response_data)
    
class RssConfigEditView(LoginRequiredMixin,TemplateView):
    """
    编辑域名
    """
    template_name = 'rss/rssconfigedit.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        得到
        """

        #记录ID
        self._id = request.GET.get('id')
        self.ormdata = Config.objects.get(id=self._id)

        return super(RssConfigEditView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            'id': self._id,
            'url': self.ormdata.url,
            'siteinfo_id': self.ormdata.siteinfo_id.id
        }
        kwargs.update(context)
        return super(RssConfigEditView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        url = request.POST.get("url").strip()
        siteinfo_id = request.POST.get("siteinfo_id").strip()

        _id = request.POST.get('id')

        ormdata_siteinfo = SiteInfo.objects.get(id=int(siteinfo_id))
        
        ormdata = Config.objects.get(id=_id)

        ormdata.url = url
        ormdata.siteinfo_id=ormdata_siteinfo

        ormdata.save()

        response_data={"code":1,"msg":"添加成功"}

        return JsonResponse(response_data)

class RssConfigDelView(LoginRequiredMixin,TemplateView):
    """
    删除
    """
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """

        #得到批量或者单个要删除的id
        ids = request.POST.getlist("ids[]")
        #print("ids====>",ids)

        Config.objects.filter(id__in=ids).delete()

        #Site.objects.filter(id=i).delete()

        response_data={"code":1,"msg":"操作成功"}


        return JsonResponse(response_data)
    
#==================
class RssRuleListView(LoginRequiredMixin,TemplateView):
    """
    显示
    """
    template_name = 'rss/rssrule.html'

    def get(self, request, *args, **kwargs):
        """
        
        """
        return super(RssRuleListView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            # 'data': self.ormdata_game
        }
        kwargs.update(context)
        return super(RssRuleListView, self).get_context_data(**kwargs)
    
    
class RssRuleAddView(LoginRequiredMixin,TemplateView):
    """
    添加
    """
    template_name = 'rss/rssruleadd.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        """
        return super(RssRuleAddView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        html_notifys = []
        notify_type = {'iyuu':'IYUU','telegram':'Telegram','email':'邮箱','enwechat':'企业微信'}

        #获取通知配置
        notifys_count = NotifyConfig.objects.count()
        if notifys_count == 0:
            html_notifys.append('<b><span style="color: red;"><font size="2">请先配置通知</font></span></b>')
        else:
            for d in NotifyConfig.objects.all():
                html_notifys.append('<input type="checkbox" name="notifys" value="' + d.name +'" title="' + notify_type[d.name] + '"/>')   
                
        context = {
            'notifys':"".join(html_notifys),
        }
        kwargs.update(context)
        return super(RssRuleAddView, self).get_context_data(**kwargs)

    #事务回滚
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        name = request.POST.get("name").strip()
        config_id = request.POST.get("config_id").strip()
        keyword = request.POST.get("keyword").strip()
        tools_id = request.POST.get("tools_id").strip()
        status = request.POST.get("status")
        refresh_time = request.POST.get("refresh_time",'')
        notifys = request.POST.getlist("notifys[]")
        rate = request.POST.get("rate").strip()
        is_paused = request.POST.get("rate")

        ormdata_config = Config.objects.get(id=int(config_id))
        ormdata_tools = Tools.objects.get(id=int(tools_id))
        #任务ID号
        crontab_id = str(uuid.uuid1())
        
        if status == "on":
            status = 1
        else:
            status = 0
            
        if refresh_time == '':
            refresh_time = 5
        
        #创建任务
        #每几分运行
        crontab_time = '*/%s * * * *' % refresh_time
        
        ormdata_job = Job.objects.create(name=name,
                                     jobtype_id=1002,
                                     crontab_time_type = "minute",
                                     crontab_status = status,
                                     minute = refresh_time,
                                     notifys = ",".join(notifys),
                                     crontab_time = crontab_time,
                                     crontab_id = crontab_id,
                                     
                                    )
        ormdata_job.save()
            
        #创建订阅规则
        ormdata_rule = Rule.objects.create(name=name,
                                      config_id=ormdata_config,
                                      tools_id=ormdata_tools,
                                      keyword=keyword,
                                      status = status,
                                      refresh_time = int(refresh_time),
                                      job_id = ormdata_job,
                                      rate = rate,
                                      is_paused = int(is_paused)
                                      )

        ormdata_rule.save()
        
        
        #开始进行订阅操作
        minute = '*/%s' % refresh_time
        my_scheduler(crontab_id, status, minute=minute, jobtype_id=1002)
        
        response_data={"code":1,"msg":"添加成功"}
        

        return JsonResponse(response_data)
    
class RssRuleEditView(LoginRequiredMixin,TemplateView):
    """
    编辑域名
    """
    template_name = 'rss/rssruleedit.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        得到
        """

        #记录ID
        self._id = request.GET.get('id')
        self.ormdata = Rule.objects.get(id=self._id)

        return super(RssRuleEditView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):
        
        html_notifys = []
        notify_type = {'iyuu':'IYUU','telegram':'Telegram','email':'邮箱','enwechat':'企业微信'}

        ormdata_job = Job.objects.get(id=self.ormdata.job_id.id)
        
        for d in NotifyConfig.objects.all():
            if d.name in ormdata_job.notifys:
                html_notifys.append('<input type="checkbox" name="notifys" value="' + d.name +'" title="' + notify_type[d.name] + '" checked />')
            else:
                html_notifys.append('<input type="checkbox" name="notifys" value="' + d.name +'" title="' + notify_type[d.name] + '"/>')
                
        context = {
            'id': self._id,
            'name': self.ormdata.name,
            'config_id': self.ormdata.config_id.id,
            'tools_id': self.ormdata.tools_id.id,
            'keyword': self.ormdata.keyword,
            'status': self.ormdata.status,
            'refresh_time': self.ormdata.refresh_time,
            'notifys':"".join(html_notifys),
            'crontab_id': ormdata_job.crontab_id,
            'rate': self.ormdata.rate,
            'is_paused':self.ormdata.is_paused
            
        }
        kwargs.update(context)
        return super(RssRuleEditView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        name = request.POST.get("name").strip()
        config_id = request.POST.get("config_id").strip()
        keyword = request.POST.get("keyword").strip()
        tools_id = request.POST.get("tools_id").strip()
        status = request.POST.get("status")
        refresh_time = request.POST.get("refresh_time",'')
        crontab_id = request.POST.get("crontab_id")
        rate = request.POST.get("rate")
        is_paused = request.POST.get("is_paused")
        notifys = request.POST.getlist("notifys[]")
        
        _id = request.POST.get('id')

        ormdata_config = Config.objects.get(id=int(config_id))
        ormdata_tools = Tools.objects.get(id=int(tools_id))
        
        if status == "on":
            status = 1
        else:
            status = 0
            
        if refresh_time == '':
            refresh_time = 5
        
        ormdata = Rule.objects.get(id=_id)

        ormdata.name = name
        ormdata.config_id=ormdata_config
        ormdata.tools_id = ormdata_tools
        ormdata.keyword = keyword
        ormdata.status = status
        ormdata.refresh_time = refresh_time
        ormdata.rate = rate
        ormdata.is_paused = int(is_paused)

        ormdata.save()
        
        crontab_time = '*/%s * * * *' % refresh_time
        Job.objects.filter(crontab_id=crontab_id).update(notifys=",".join(notifys),
                                                         crontab_time = crontab_time,
                                                         minute = refresh_time
                                                         )
        
        minute = '*/%s' % refresh_time
        my_scheduler(crontab_id = crontab_id, crontab_status = status, minute=minute,  jobtype_id=1002 )        

        response_data={"code":1,"msg":"添加成功"}

        return JsonResponse(response_data)

class RssRuleDelView(LoginRequiredMixin,TemplateView):
    """
    删除
    """
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """

        #得到批量或者单个要删除的id
        ids = request.POST.getlist("ids[]")
        #print("ids====>",ids)

        #Rule.objects.filter(id__in=ids).delete()
        
        for i in ids:
            _id = Rule.objects.get(id=i)
            #删除任务
            Job.objects.filter(id=_id.job_id.id).delete()
            #删除记录
            Rule.objects.filter(id=i).delete()
            #删除计划任务
            my_scheduler(crontab_id = _id.job_id.crontab_id, action="del")

        response_data={"code":1,"msg":"操作成功"}


        return JsonResponse(response_data)
    
#==================
class RssSeedInfoListView(LoginRequiredMixin,TemplateView):
    """
    显示
    """
    template_name = 'rss/rssseedinfo.html'

    def get(self, request, *args, **kwargs):
        """
        
        """
        return super(RssSeedInfoListView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            # 'data': self.ormdata_game
        }
        kwargs.update(context)
        return super(RssSeedInfoListView, self).get_context_data(**kwargs)
    

class RssSeedInfoDelView(LoginRequiredMixin,TemplateView):
    """
    删除
    """
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """

        #得到批量或者单个要删除的id
        ids = request.POST.getlist("ids[]")
        #print("ids====>",ids)

        SeedInfo.objects.filter(id__in=ids).delete()

        response_data={"code":1,"msg":"操作成功"}


        return JsonResponse(response_data)
    
#==================