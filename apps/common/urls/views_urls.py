# coding:utf-8
from django.urls import path
from .. import views, views_request

app_name = 'common'

urlpatterns = [
    # Resource asset path

    #百度ocr
    #path('baiduocr', views.BaiDuOcrView.as_view()),
    #备份恢复
    path('backupload', views.BackupLoadView.as_view()),
    path('backup', views_request.backup),
    #补签
    path('signagain', views_request.signAgain),
    path('signcheck', views_request.signCheck),
    
]

