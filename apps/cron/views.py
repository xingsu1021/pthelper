from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from django.conf import settings
import time
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from django_apscheduler.jobstores import DjangoJobStore, register_job
from .models import JobType, Job
from notify.models import NotifyConfig
from .crontabs import *

import logging
import uuid

logger = logging.getLogger('django')

executors = {
    # 执行器的线程与进程数
    'default': ThreadPoolExecutor(10),
    'processpool': ProcessPoolExecutor(10)
}

jobstores = {
    'default': DjangoJobStore()
}

job_defaults = {
    # 最近多久时间内允许存在的任务数
    'misfire_grace_time': 10,
    # 该定时任务允许最大的实例个数
    'max_instances': 2,
    # 是否运行一次最新的任务，当多个任务堆积时
    #'coalesce': True,
    #存在相同任务直接覆盖
    'replace_existing': True,
}

# 1.实例化调度器
scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE,job_defaults=job_defaults)
# 2.调度器使用DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), "default")
# 5.开启定时任务
scheduler.start()
#try:
    ## 3.设置定时任务
    ## 另一种方式为每天固定时间执行任务，对应代码为
    #@register_job(scheduler,"cron", second="*/10",id="test", replace_existing=True)
    #def my_job():
        ## 这里写你要执行的任务
        #format_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        #print(format_time)
    ## 5.开启定时任务
    #scheduler.start()
    #print("Scheduler started!")
#except Exception as e:
    #print(e)
    ## 有错误就停止定时器
    #scheduler.shutdown()
    
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

        context = {
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
        week = request.POST.get("week",0)
        day = request.POST.get("day",0)
        hour = request.POST.get("hour",0)
        minute = request.POST.get("minute",0)
        second = request.POST.get("second",0)
        crontab_time_type = request.POST.get("select")
        sites = request.POST.getlist("sites")

        if crontab_time_type == 'day':
            #每天几点几分运行
            crontab_time = minute + ' ' + hour + '* * *'
            

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
                                         sites = ",".join(sites),
                                         crontab_time = crontab_time,
                                         crontab_id = uuid.uuid1()
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
    
class JobEditView(LoginRequiredMixin,TemplateView):
    """
    编辑域名
    """
    template_name = 'cron/jobedit.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        得到
        """

        #记录ID
        self._id = request.GET.get('id')
        self.ormdata = JobType.objects.get(id=self._id)

        return super(JobEditView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            'id': self._id,
            'name': self.ormdata.name,
            'type_id': self.ormdata.type_id,

        }
        kwargs.update(context)
        return super(JobEditView, self).get_context_data(**kwargs)

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

        Job.objects.filter(id__in=ids).delete()

        #Site.objects.filter(id=i).delete()

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
        crontab_time = minute + ' ' + hour + '* * *'
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
        
        # 创建任务
        #scheduler.add_job(test, 'cron', hour=hour, minute=minute, second=second, args=[s])
        isJob = scheduler.get_job(crontab_id)

        if isJob != None:

            #激活
            if crontab_status == '1':
                #已经存在的任务不能做时间修改，必须删除在添加
                scheduler.remove_job(crontab_id)
                scheduler.add_job(sign, 'cron', hour=hour, minute=minute, id=crontab_id, args=[crontab_id])

            else:
                #禁用状态，直接删除任务
                scheduler.remove_job(crontab_id)
                #暂停任务
                #scheduler.pause_job(crontab_id)

        else:
            #启用添加，禁用忽略
            if crontab_status == '1':
                scheduler.add_job(sign, 'cron', hour=hour, minute=minute, id=crontab_id, args=[crontab_id])

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