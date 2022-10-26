# coding:utf-8
from django.urls import path
from .. import views, views_request

app_name = 'sites'

urlpatterns = [
    # Resource asset path

    #站点配置
    path('siteconfig', views.SiteConfigListView.as_view()),
    path('siteconfig/add', views.SiteConfigAddView.as_view()),
    path('siteconfig/edit', views.SiteConfigEditView.as_view()),
    path('siteconfig/del', views.SiteConfigDelView.as_view()),
    path('siteconfig/list', views_request.siteconfig),
    path('siteconfigname/list', views_request.siteconfigname),
    path('siteconfig/export', views_request.siteconfigExport),
    path('siteconfig/import', views_request.siteconfigImport),    
    #站点升级配置
    path('siterankconfig', views.SiteRankConfigListView.as_view()),
    path('siterankconfig/add', views.SiteRankConfigAddView.as_view()),
    path('siterankconfig/edit', views.SiteRankConfigEditView.as_view()),
    path('siterankconfig/del', views.SiteRankConfigDelView.as_view()),
    path('siterankconfig/list', views_request.siterankconfig),
    #站点信息
    path('siteinfo', views.SiteInfoListView.as_view()),
    path('siteinfo/add', views.SiteInfoAddView.as_view()),
    path('siteinfo/edit', views.SiteInfoEditView.as_view()),
    path('siteinfo/del', views.SiteInfoDelView.as_view()),
    path('siteinfo/list', views_request.siteinfo),
    path('siteinfo/export', views_request.siteinfoExport),
    path('siteinfo/import', views_request.siteinfoImport),
    path('siteinfo/select/list', views_request.select_siteinfo),
    #站点代理配置
    path('siteproxy', views.SiteProxyListView.as_view()),
    path('siteproxy/add', views.SiteProxyAddView.as_view()),
    path('siteproxy/edit', views.SiteProxyEditView.as_view()),
    path('siteproxy/del', views.SiteProxyDelView.as_view()),
    path('siteproxy/list', views_request.siteproxy),
    path('siteproxy/select/list', views_request.select_siteproxy),
    #用戶信息
    path('siteuser', views_request.siteuser),
    path('siteuser/update', views_request.getUserInfo),
    
]

