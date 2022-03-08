# coding:utf-8
from django.urls import path
from .. import views

app_name = 'dashboard'

urlpatterns = [
    # Resource asset url
    path('', views.DashboardListView.as_view(), name='dashboard'),

]

