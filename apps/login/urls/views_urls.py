# coding:utf-8
from django.urls import path
from .. import views

app_name = 'login'

urlpatterns = [
    # Resource asset url
    path('login', views.LoginView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout', views.logout),

]

