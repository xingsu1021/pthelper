# coding:utf-8
from django.urls import path
from .. import views, views_request

app_name = 'mymenu'

urlpatterns = [
    # Resource asset url

    path('index/', views.MenuListView.as_view()),
    path('add', views.MenuAddView.as_view()),
    path('edit', views.MenuEditView.as_view()),
    path('del', views.MenuDelView.as_view()),

    path('list/', views_request.menu),
    path('groupmenuztree/', views_request.groupmenuztree),
    path('usermenuztree/', views_request.usermenuztree),
    path('menuztree/', views_request.menuztree),

]

