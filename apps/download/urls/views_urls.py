# coding:utf-8
from django.urls import path
from .. import views, views_request

app_name = 'download'

urlpatterns = [
    # Resource asset path

    #下载器配置

    path('tools', views.ToolsListView.as_view()),
    path('tools/add', views.ToolsAddView.as_view()),
    path('tools/edit', views.ToolsEditView.as_view()),
    path('tools/del', views.ToolsDelView.as_view()),
    path('tools/list', views_request.tools),
    path('tools/select/list', views_request.select_tools),
    path('tools/test', views_request.tools_test),
    
]

