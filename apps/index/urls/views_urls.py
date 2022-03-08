# coding:utf-8
from django.urls import path
from .. import views

app_name = 'index'

urlpatterns = [
    # Resource asset url
    path('', views.IndexView.as_view()),
    path('index/theme', views.IndexThemeView.as_view()),
    path('index/note', views.IndexNoteView.as_view()),
    path('index/message', views.IndexMessageView.as_view()),
    path('index/about', views.IndexAboutView.as_view()),
]

