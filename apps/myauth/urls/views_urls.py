# coding:utf-8
from django.urls import path
from .. import views, views_request

app_name = 'myauth'

urlpatterns = [
    # Resource asset url
    path('user', views.UserListView.as_view(), name='user'),
    path('user/add', views.UserAddView.as_view(), name='useradd'),
    path('user/edit', views.UserEditView.as_view(), name='useredit'),
    path('user/del', views.UserDelView.as_view(), name='userdel'),
    path('user/resetpasswd', views.UserResetPasswdView.as_view(), name='resetpasswd'),
    path('user/resetpasswd2', views.UserResetPasswd2View.as_view()),
    path('user/resetaccount', views.UserResetAccountView.as_view()),
    

    path('group/', views.GroupListView.as_view()),
    path('group/add', views.GroupAddView.as_view()),
    path('group/edit', views.GroupEditView.as_view()),
    #path('group/del', views.GroupDelView.as_view()),
    path('group/groupusersadd', views.GroupUsersAddView.as_view()),

    path('permission/', views.PermissionListView.as_view()),
    path('permissiongroup/add', views.PermissionGroupAddView.as_view()),
    path('permissionuser/add', views.PermissionUserAddView.as_view()),

    #
    path('myuser/list', views_request.user),
    path('group/list', views_request.group),
    path('permissiongroup/list', views_request.permissiongroup),
    path('permissionuser/list', views_request.permissionuser),
    path('myuser/setvalue', views_request.setValue),

]

