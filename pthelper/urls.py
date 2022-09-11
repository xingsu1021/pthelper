"""pthelper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #path('api-auth/', include('rest_framework.urls')),
    
    #index
    path('', include('index.urls.views_urls')),
    #登录
    path('', include('login.urls.views_urls')),
    #Dashboard
    path('dashboard', include('dashboard.urls.views_urls')),
    #用户、组、权限
    path('myauth/', include('myauth.urls.views_urls')),
    #菜单
    path('mymenu', include('mymenu.urls.views_urls')),    
    #站点管理
    path('sites/', include('sites.urls.views_urls')), 
    #任务管理
    path('cron/', include('cron.urls.views_urls')), 
    #消息通知
    path('notify/', include('notify.urls.views_urls')), 
    #通用配置
    path('common/', include('common.urls.views_urls')), 
    #RSS订阅
    path('rss/', include('rss.urls.views_urls')),
    #下载工具管理
    path('download/', include('download.urls.views_urls')),        
]
