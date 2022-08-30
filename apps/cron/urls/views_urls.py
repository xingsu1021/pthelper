# coding:utf-8
from django.urls import path
from .. import views, views_request

app_name = 'cron'

urlpatterns = [
    # Resource asset path

    #任务类型
    path('jobtype', views.JobTypeListView.as_view()),
    path('jobtype/add', views.JobTypeAddView.as_view()),
    path('jobtype/edit', views.JobTypeEditView.as_view()),
    path('jobtype/del', views.JobTypeDelView.as_view()),
    path('jobtype/list', views_request.jobtype),
    path('jobtypeinfo/list', views_request.jobtypeinfo),
    path('jobtimetype/list', views_request.jobtimetype),
    
    #任务
    path('job', views.JobListView.as_view()),
    path('job/add', views.JobAddView.as_view()),
    path('job/edit', views.JobEditView.as_view()),
    path('job/del', views.JobDelView.as_view()),
    path('job/list', views_request.job),
    #签到任务
    path('sign', views.SignJobView.as_view()),
    #日志
    path('log', views.LogListView.as_view()),
    path('log/del', views.LogDelView.as_view()),
    path('log/list', views_request.log),
    path('loginfo', views_request.loginfo),
    
]

