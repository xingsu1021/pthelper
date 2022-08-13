# coding:utf-8
from django.urls import path
from .. import views, views_request

app_name = 'notify'

urlpatterns = [
    # Resource asset path

    #消息通知
    path('iyuu', views.IyuuView.as_view()),
    path('iyuutest', views_request.iyuutest),
    path('telegram', views.TelegramView.as_view()),
    path('telegramtest', views_request.telegramtest),
    path('email', views.EmailView.as_view()),
    path('emailtest', views_request.emailtest),   
    path('mailtype/list', views_request.mailtypeinfo),
    path('enwechat', views.EnWechatView.as_view()),
    path('enwechattest', views_request.enwechattest),     
]

