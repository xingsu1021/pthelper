# coding:utf-8
from django.urls import path
from .. import views, views_request

app_name = 'common'

urlpatterns = [
    # Resource asset path

    #百度ocr
    #path('baiduocr', views.BaiDuOcrView.as_view()),
    #备份恢复
    path('backup', views.BackupView.as_view()),
    path('backup/export', views_request.backupExport),
    path('backup/import', views_request.backupImport),
    #补签
    path('signagain', views_request.signAgain),
    path('signcheck', views_request.signCheck),
    #升级
    path('update', views.UpdateView.as_view()),
    
]

