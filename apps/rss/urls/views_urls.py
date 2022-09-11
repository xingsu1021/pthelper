# coding:utf-8
from django.urls import path
from .. import views, views_request

app_name = 'rss'

urlpatterns = [
    # Resource asset path

    #RSS配置
    path('config', views.RssConfigListView.as_view()),
    path('config/add', views.RssConfigAddView.as_view()),
    path('config/edit', views.RssConfigEditView.as_view()),
    path('config/del', views.RssConfigDelView.as_view()),
    path('config/list', views_request.config),
    path('config/select/list', views_request.select_rssconfig),
    
    #RSS规则
    path('rule', views.RssRuleListView.as_view()),
    path('rule/add', views.RssRuleAddView.as_view()),
    path('rule/edit', views.RssRuleEditView.as_view()),
    path('rule/del', views.RssRuleDelView.as_view()),
    path('rule/list', views_request.rule),
    path('rule/checkbox/setstatus', views_request.checkbox_setRuleStatus),
    
    #RSS种子详情
    path('seedinfo', views.RssSeedInfoListView.as_view()),
    path('seedinfo/del', views.RssSeedInfoDelView.as_view()),
    path('seedinfo/list', views_request.seedinfo),
    path('seedinfo/donwload', views_request.seed_download),
]

