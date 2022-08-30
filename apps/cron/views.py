from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

import sys

from .models import JobType, Job
from notify.models import NotifyConfig
from sites.models import SiteInfo,SiteConfig
from cron.models import Job
from .crontabs import my_scheduler

import logging
import uuid

logger = logging.getLogger('django')


    
class JobTypeListView(LoginRequiredMixin,TemplateView):
    """
    显示
    """
    template_name = 'cron/jobtype.html'

    def get(self, request, *args, **kwargs):
        """
        
        """
        return super(JobTypeListView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            # 'data': self.ormdata_game
        }
        kwargs.update(context)
        return super(JobTypeListView, self).get_context_data(**kwargs)
    
    
class JobTypeAddView(LoginRequiredMixin,TemplateView):
    """
    添加
    """
    template_name = 'cron/jobtypeadd.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        """
        return super(JobTypeAddView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
        }
        kwargs.update(context)
        return super(JobTypeAddView, self).get_context_data(**kwargs)


    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        name = request.POST.get("name").strip()
        type_id = request.POST.get("type_id").strip()


        try:
            ormdata = JobType.objects.create(name=name,
                                            type_id=type_id,
                                                )            
            ormdata.save()
            response_data={"code":1,"msg":"添加成功"}
        except:
            ex_type, ex_val, ex_stack = sys.exc_info()

            if 'UNIQUE' in str(ex_val):
                response_data={"code":0,"msg":"存在相同记录"}
            else:
                response_data={"code":0,"msg":"操作失败,请联系管理员"}
        

        return JsonResponse(response_data)
    
class JobTypeEditView(LoginRequiredMixin,TemplateView):
    """
    编辑域名
    """
    template_name = 'cron/jobtypeedit.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        得到
        """

        #记录ID
        self._id = request.GET.get('id')
        self.ormdata = JobType.objects.get(id=self._id)

        return super(JobTypeEditView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            'id': self._id,
            'name': self.ormdata.name,
            'type_id': self.ormdata.type_id,

        }
        kwargs.update(context)
        return super(JobTypeEditView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        name = request.POST.get("name").strip()
        type_id = request.POST.get("type_id").strip()

        _id = request.POST.get('id')

        ormdata = JobType.objects.get(id=_id)

        ormdata.name = name
        ormdata.type_id = type_id

        ormdata.save()

        response_data={"code":1,"msg":"添加成功"}

        return JsonResponse(response_data)

class JobTypeDelView(LoginRequiredMixin,TemplateView):
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

        JobType.objects.filter(id__in=ids).delete()

        #Site.objects.filter(id=i).delete()

        response_data={"code":1,"msg":"操作成功"}


        return JsonResponse(response_data)
    
#===================================================================
class JobListView(LoginRequiredMixin,TemplateView):
    """
    显示
    """
    template_name = 'cron/job.html'

    def get(self, request, *args, **kwargs):
        """
        
        """
        return super(JobListView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            # 'data': self.ormdata_game
        }
        kwargs.update(context)
        return super(JobListView, self).get_context_data(**kwargs)
    
    
class JobAddView(LoginRequiredMixin,TemplateView):
    """
    添加
    """
    template_name = 'cron/jobadd.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        """
        return super(JobAddView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):
        html = []
        notify_type = {'iyuu':'IYUU','telegram':'Telegram','email':'邮箱','enwechat':'企业微信'}

        #获取通知配置
        notifys_count = NotifyConfig.objects.count()
        if notifys_count == 0:
            html.append('<b><span style="color: red;"><font size="2">请先配置通知</font></span></b>')
        else:
            for d in NotifyConfig.objects.all():
                html.append('<input type="checkbox" name="notifys" value="' + d.name +'" title="' + notify_type[d.name] + '"/>')                
            
        siteinfo_html = []
        siteinfo_count = SiteInfo.objects.count()
        if siteinfo_count == 0:
            siteinfo_html.append('<b><span style="color: red;"><font size="2">请先配置通知</font></span></b>')
        else:
            for d in SiteInfo.objects.all():
                if d.siteconfig_name_cn == '' or d.siteconfig_name_cn == None:
                    s = SiteConfig.objects.get(name=d.siteconfig_name)
                    name_cn = s.name_cn
                    
                    SiteInfo.objects.filter(siteconfig_name=d.siteconfig_name).update(siteconfig_name_cn = name_cn)
                else:
                    name_cn = d.siteconfig_name_cn
                    
                siteinfo_html.append('<input type="checkbox" name="sites" value="' + d.siteconfig_name +'" title="' + d.siteconfig_name + "(" + name_cn + ")" + '"/>')   
                        
        context = {
            'notifys':"".join(html),
            'sites':"".join(siteinfo_html)
        }
        
        kwargs.update(context)
        return super(JobAddView, self).get_context_data(**kwargs)


    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        name = request.POST.get("name").strip()
        jobtype_id = request.POST.get("job_type")
        crontab_status = request.POST.get("crontab_status")
        week = request.POST.get("week",'*')
        day = request.POST.get("day",'*')
        hour = request.POST.get("hour",'*')
        minute = request.POST.get("minute",'*')
        second = request.POST.get("second",'*')
        crontab_time_type = request.POST.get("select")
        sites = request.POST.getlist("sites")
        notifys = request.POST.getlist("notifys")

        if crontab_time_type == 'day':
            #每天几点几分运行
            crontab_time =  '%s %s * * *' % (minute, hour)
        elif crontab_time_type == 'hour':
            #每小时几分运行
            crontab_time = '%s * * * *' % minute
        elif crontab_time_type == 'minute_n':
            #每几分运行
            crontab_time = '*/%s * * * *' % minute
            
            
        #转换uuid为字符串
        crontab_id = str(uuid.uuid1())
        
        try:
            ormdata = Job.objects.create(name=name,
                                         jobtype_id=jobtype_id,
                                         crontab_time_type = crontab_time_type,
                                         crontab_status = crontab_status,
                                         week = week,
                                         day = day,
                                         hour = hour,
                                         minute = minute,
                                         second = second,
                                         notifys = ",".join(notifys),
                                         sites = ",".join(sites),
                                         crontab_time = crontab_time,
                                         crontab_id = crontab_id
                                        )            
            ormdata.save()
            response_data={"code":1,"msg":"添加成功"}
            
            # 创建任务
            if crontab_time_type == 'minute_n':
                my_scheduler(crontab_id, int(crontab_status), hour, str(hour) +'/'+ str(minute), int(jobtype_id))
            else:
                my_scheduler(crontab_id, int(crontab_status), hour, minute, int(jobtype_id))
            
        except:
            ex_type, ex_val, ex_stack = sys.exc_info()
            
            logger.error(str(ex_val))
            
            if 'UNIQUE' in str(ex_val):
                response_data={"code":0,"msg":"存在相同记录"}
            else:
                response_data={"code":0,"msg":"操作失败,请联系管理员"}
        

        return JsonResponse(response_data)
    
class JobEditView(LoginRequiredMixin,TemplateView):
    """
    编辑任务
    """
    template_name = 'cron/jobedit.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        得到
        """

        #记录ID
        self._id = request.GET.get('id')
        self.ormdata = Job.objects.get(id=self._id)

        return super(JobEditView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):
        
        html = []
        notify_type = {'iyuu':'IYUU','telegram':'Telegram','email':'邮箱','enwechat':'企业微信'}

        for d in NotifyConfig.objects.all():
            if d.name in self.ormdata.notifys:
                html.append('<input type="checkbox" name="notifys" value="' + d.name +'" title="' + notify_type[d.name] + '" checked />')
            else:
                html.append('<input type="checkbox" name="notifys" value="' + d.name +'" title="' + notify_type[d.name] + '"/>')
            
        siteinfo_html = []

        for d in SiteInfo.objects.all():
            if d.siteconfig_name_cn == '' or d.siteconfig_name_cn == None:
                s = SiteConfig.objects.get(name=d.siteconfig_name)
                name_cn = s.name_cn
                
                SiteInfo.objects.filter(siteconfig_name=d.siteconfig_name).update(siteconfig_name_cn = name_cn)
            else:
                name_cn = d.siteconfig_name_cn
            if self.ormdata.sites == '' or self.ormdata.sites == None or d.siteconfig_name in self.ormdata.sites:
                siteinfo_html.append('<input type="checkbox" name="sites" value="' + d.siteconfig_name +'" title="' + d.siteconfig_name + "(" + name_cn + ")" + '" checked />')
            else:
                siteinfo_html.append('<input type="checkbox" name="sites" value="' + d.siteconfig_name +'" title="' + d.siteconfig_name + "(" + name_cn + ")" + '" />')
                
        context = {
            'id': self._id,
            'name': self.ormdata.name,
            'type_id': self.ormdata.jobtype_id,
            'crontab_status': self.ormdata.crontab_status,
            'notifys':"".join(html),
            'sites':"".join(siteinfo_html),
            'crontab_time_type': self.ormdata.crontab_time_type,
            'week': self.ormdata.week,
            'day': self.ormdata.day,
            'hour': self.ormdata.hour,
            'minute': self.ormdata.minute,
            'second': self.ormdata.second,
            'crontab_id': self.ormdata.crontab_id
        }
        
        kwargs.update(context)
        return super(JobEditView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        _id = request.POST.get('id','')
        name = request.POST.get("name").strip()
        jobtype_id = request.POST.get("job_type")
        crontab_status = request.POST.get("crontab_status")
        week = request.POST.get("week",'*')
        day = request.POST.get("day",'*')
        hour = request.POST.get("hour",'*')
        minute = request.POST.get("minute",'*')
        second = request.POST.get("second",'*')
        crontab_time_type = request.POST.get("select")
        sites = request.POST.getlist('sites[]')
        notifys = request.POST.getlist('notifys[]')
        crontab_id = request.POST.get("crontab_id")
        
        if crontab_time_type == 'day':
            #每天几点几分运行
            crontab_time =  '%s %s * * *' % (str(minute), str(hour))
        elif crontab_time_type == 'hour':
            #每小时几分运行
            crontab_time = '%s * * * *' % str(minute)
        elif crontab_time_type == 'minute_n':
            #每几分运行
            crontab_time = '*/%s * * * *' % str(minute)

        try:
            ormdata = Job.objects.get(id=_id)
            ormdata.name = name
            ormdata.crontab_status = crontab_status
            ormdata.week = week
            ormdata.day = day
            ormdata.hour = hour
            ormdata.minute = minute
            ormdata.second = second
            ormdata.crontab_time = crontab_time
            ormdata.crontab_time_type = crontab_time_type
            
            ormdata.notifys = ",".join(notifys)
            ormdata.sites = ",".join(sites)
        
            ormdata.save()
            
            response_data={"code":1,"msg":"编辑成功"}
            
            # 创建任务
            if crontab_time_type == 'minute_n':
                my_scheduler(crontab_id, int(crontab_status), hour, str(hour) +'/'+ str(minute), int(jobtype_id))
            else:
                my_scheduler(crontab_id, int(crontab_status), hour, minute, int(jobtype_id))
            
        except:
            ex_type, ex_val, ex_stack = sys.exc_info()

            if 'UNIQUE' in str(ex_val):
                response_data={"code":0,"msg":"存在相同记录"}
            else:
                response_data={"code":0,"msg":"操作失败,请联系管理员"}


        return JsonResponse(response_data)

class JobDelView(LoginRequiredMixin,TemplateView):
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

        ormdata = Job.objects.filter(id__in=ids)

        #删除任务
        for i in ormdata:
            my_scheduler(crontab_id=i.crontab_id, action='del')
        
        Job.objects.filter(id__in=ids).delete()

        response_data={"code":1,"msg":"操作成功"}


        return JsonResponse(response_data)
    
    
#------------------------------
class SignJobView(LoginRequiredMixin,TemplateView):
    """
    签到任务
    """
    template_name = 'cron/sign.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        得到
        """

        return super(SignJobView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):
        
        html = []
        notify_type = {'iyuu':'IYUU','telegram':'Telegram','email':'邮箱','enwechat':'企业微信'}
        #获取记录
        sign_count = Job.objects.filter(jobtype_id=1000).count()
        if sign_count == 0:
            
            #获取通知配置
            notifys_count = NotifyConfig.objects.count()
            if notifys_count == 0:
                html.append('<b><span style="color: red;"><font size="2">请先配置通知</font></span></b>')
            else:
                for d in NotifyConfig.objects.all():
                    html.append('<input type="checkbox" name="notifys[]" value="' + d.name +'" title="' + notify_type[d.name] + '"/>')                
                
            context = {'notifys':"".join(html),
            }
        else:
            #获取通知配置
            notifys_count = NotifyConfig.objects.count()
            ormdata = Job.objects.get(jobtype_id=1000)
            if notifys_count == 0:
                html.append('<p>请先配置通知</p>')
            else:
                #notify_ormdata = NotifyConfig.objects.all()
                       
                for d in NotifyConfig.objects.all():
                    
                    if ormdata.notifys == None:
                        html.append('<input type="checkbox" name="notifys[]" value="' + d.name +'" title="' + notify_type[d.name] + '"/>')                    
                    elif d.name in ormdata.notifys:
                        html.append('<input type="checkbox" name="notifys[]" value="' + d.name +'" title="' + notify_type[d.name] + '" checked />')
                    else:
                        html.append('<input type="checkbox" name="notifys[]" value="' + d.name +'" title="' + notify_type[d.name] + '"/>')

            
            context = {
                'id': ormdata.id,
                'jobtype_id': ormdata.jobtype_id,
                'hour':ormdata.hour,
                'minute':ormdata.minute,
                'crontab_status':ormdata.crontab_status,
                'notifys':"".join(html),
                'crontab_id': ormdata.crontab_id
            }
        kwargs.update(context)
        return super(SignJobView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        _id = request.POST.get('id','')
        crontab_status = request.POST.get("crontab_status")
        hour = request.POST.get("hour")
        minute = request.POST.get("minute")
        #需要html配合
        notifys = request.POST.getlist('notifys[]')
        crontab_id = request.POST.get("crontab_id",'')
        
        if crontab_id == "" or crontab_id == None:
            crontab_id = str(uuid.uuid1())

        jobtype_id = 1000
        crontab_time_type = 'day'
        #每天几点几分运行
        crontab_time = minute + ' ' + hour + ' * * *'
        name = "签到"
        
        #未配置消息通知不予通过
        if len(notifys) == 0:
            response_data={"code":0,"msg":"请配置消息通知!"}
            return JsonResponse(response_data)

        data_count = Job.objects.filter(jobtype_id=1000).count()
        if data_count == 0:
            ormdata = Job.objects.create(name=name,
                                         crontab_status=crontab_status,
                                         hour=hour,
                                         minute=minute,
                                         jobtype_id=jobtype_id,
                                         crontab_time_type=crontab_time_type,
                                         crontab_time=crontab_time,
                                         crontab_id = crontab_id,
                                         notifys = ",".join(notifys)
                                         )
        else:
            ormdata = Job.objects.get(id=_id)
            ormdata.crontab_status = crontab_status
            ormdata.hour = hour
            ormdata.minute = minute
            ormdata.crontab_time = crontab_time
            ormdata.notifys = ",".join(notifys)

        ormdata.save()
        
        crontab_id = ormdata.crontab_id
        crontab_status = ormdata.crontab_status
        
        # 创建任务
        my_scheduler(crontab_id, crontab_status, hour, minute, jobtype_id)


        response_data={"code":1,"msg":"添加成功"}

        return JsonResponse(response_data)
    
#===================================================================
class LogListView(LoginRequiredMixin,TemplateView):
    """
    显示
    """
    template_name = 'cron/log.html'

    def get(self, request, *args, **kwargs):
        """
        
        """
        return super(LogListView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            # 'data': self.ormdata_game
        }
        kwargs.update(context)
        return super(LogListView, self).get_context_data(**kwargs)
    
class LogDelView(LoginRequiredMixin,TemplateView):
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

        Log.objects.filter(id__in=ids).delete()

        #Site.objects.filter(id=i).delete()

        response_data={"code":1,"msg":"操作成功"}


        return JsonResponse(response_data)