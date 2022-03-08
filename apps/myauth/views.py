from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import check_password, make_password, is_password_usable
from django.db import IntegrityError
import sys
import traceback
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth.mixins import LoginRequiredMixin
import simplejson as json
from .models import User, Group
from mymenu.models import Menu
from myauth.mixins import AdminUserRequiredMixin
from rest_framework.authtoken.models import Token

import logging
# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)

# Create your views here.
#class UserListView(LoginRequiredMixin, TemplateView):
class UserListView(AdminUserRequiredMixin,TemplateView):
    """
    显示用户列表
    """
    template_name = 'myauth/user.html'

    def get_context_data(self, **kwargs):
        context = {
            # 'app': 'Assets',
            # 'action': 'Asset list',
        }
        kwargs.update(context)
        return super(UserListView, self).get_context_data(**kwargs)

class UserAddView(AdminUserRequiredMixin,TemplateView):
    """
    添加用户
    """
    template_name = 'myauth/useradd.html'
    model = User

    #显示添加模板
    def get_context_data(self, **kwargs):
        context = {
            # 'app': 'Assets',
            # 'action': 'Asset list',
        }
        kwargs.update(context)
        return super(UserAddView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        name = request.POST.get("name")
        password = request.POST.get("password")
        nickname = request.POST.get("nickname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        is_superuser = request.POST.get("is_superuser")
        is_active = request.POST.get("is_active")

        msg=""
        try:
            ormdata = self.model.objects.create(name=name,
                                    password=make_password(password),
                                    nickname=nickname,
                                    email=email,
                                    mobile=mobile,
                                    is_superuser=is_superuser,
                                    is_active=is_active
                                    )
            ormdata.save()
            data={"code":1,"msg":"添加成功"}
        except IntegrityError as e:
            #得到异常消息
            msg=str(e)
            #msg = "用户或邮箱已经存在"
            logger.error(e.__cause__)
            data={"code":0,"msg":msg}

        return JsonResponse(data)

class UserEditView(AdminUserRequiredMixin,TemplateView):
    """
    编辑用户
    """
    template_name = 'myauth/useredit.html'
    model = User

    def get(self, request, *args, **kwargs):
        """
        得到提交的id
        """
        _id = request.GET.get('id')
        #根据id得到数据
        ormdata = self.model.objects.get(id=_id)
        self.id = ormdata.id
        self.name = ormdata.name
        self.nickname = ormdata.nickname
        self.email = ormdata.email
        self.mobile = ormdata.mobile
        self.is_superuser = ormdata.is_superuser
        self.is_active = ormdata.is_active
        return super(UserEditView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):
        context = {
            'id': self.id,
            'name': self.name,
            'nickname': self.nickname,
            'email': self.email,
            'mobile': self.mobile,
            'is_superuser': self.is_superuser,
            'is_active': self.is_active,
        }
        kwargs.update(context)
        return super(UserEditView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        _id = request.POST.get('id')
        name = request.POST.get("name")
        nickname = request.POST.get("nickname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        is_superuser = request.POST.get("is_superuser")
        is_active = request.POST.get("is_active")

        msg=""
        try:
            ormdata = self.model.objects.get(id=_id)
            ormdata.name=name
            ormdata.nickname=nickname
            ormdata.email=email
            ormdata.mobile=mobile
            ormdata.is_superuser=is_superuser
            ormdata.is_active=is_active

            ormdata.save()
            data={"code":1,"msg":"修改成功"}
        except IntegrityError as e:
            #得到异常消息
            msg=str(e)
            logger.error(e)
            data={"code":0,"msg":msg}

        return JsonResponse(data)

class UserDelView(AdminUserRequiredMixin,TemplateView):
    """
    删除用户(用户只能禁用，不能删除)
    """
    model = User

    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        #得到批量或者单个要删除的id
        ids = request.POST.getlist("ids[]")

        #删除管理员id，管理员id为1禁止删除
        admin_id = 1
        if admin_id in ids:
            ids.remove(admin_id)

        #禁止删除自身
        my_id = request.user.id
        if my_id in ids:
            ids.remove(my_id)

        msg=""
        #批量删除，使用in方法
        #self.model.objects.filter(id__in=ids).delete()
        self.model.objects.filter(id__in=ids).update(is_active=0,is_delete=1)
        Token.objects.filter(user_id__in=ids).delete()
        data={"code":1,"msg":"删除成功"}

        return JsonResponse(data)

class UserResetPasswdView(AdminUserRequiredMixin,TemplateView):
    """
    用户密码重置
    """
    template_name = 'myauth/resetpasswd.html'
    model = User

    def get(self, request, *args, **kwargs):
        """
        得到提交的ids
        """
        self.id = request.GET.get('id')

        return super(UserResetPasswdView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):
        context = {
            'id': self.id
        }
        kwargs.update(context)
        return super(UserResetPasswdView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        _id = request.POST.get('id')
        password = request.POST.get("password")

        msg=""
        try:
            # ormdata = self.model.objects.get(id=_id)
            # ormdata.password=make_password(password)

            # ormdata.save()
            self.model.objects.filter(id=_id).update(password=make_password(password))
            data={"code":1,"msg":"密码修改成功"}
        except IntegrityError as e:
            #得到异常消息
            msg=str(e)
            logger.error(msg)
            data={"code":0,"msg":msg}

        return JsonResponse(data)
        #return HttpResponse(json.dumps(data,ensure_ascii = False), "text/html")

class UserResetPasswd2View(AdminUserRequiredMixin,TemplateView):
    """
    用户密码重置
    """
    template_name = 'myauth/resetpasswd.html'
    model = User

    def get(self, request, *args, **kwargs):
        """
        得到提交的ids
        """
        self.user = request.user

        return super(UserResetPasswd2View, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):
        context = {
            'id': self.user.id
        }
        kwargs.update(context)
        return super(UserResetPasswd2View, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        _id = request.POST.get('id')
        password = request.POST.get("password")

        msg=""
        try:
            # ormdata = self.model.objects.get(id=_id)
            # ormdata.password=make_password(password)

            # ormdata.save()
            self.model.objects.filter(id=_id).update(password=make_password(password))
            data={"code":1,"msg":"密码修改成功"}
        except IntegrityError as e:
            #得到异常消息
            msg=str(e)
            logger.error(msg)
            data={"code":0,"msg":msg}

        return JsonResponse(data)
    
#--------------------------------------------------------------
class UserResetAccountView(LoginRequiredMixin,TemplateView):
    """
    重置账号信息
    """
    template_name = 'myauth/resetaccount.html'
    model = User

    def get(self, request, *args, **kwargs):
        """
        得到提交的ids
        """
        self.id = request.user.id

        return super(UserResetAccountView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):
        context = {
            'id': self.id
        }
        kwargs.update(context)
        return super(UserResetAccountView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        _id = request.POST.get('id')
        name = request.POST.get("name")
        password = request.POST.get("password")

        msg=""
        try:
            # ormdata = self.model.objects.get(id=_id)
            # ormdata.password=make_password(password)

            # ormdata.save()
            self.model.objects.filter(id=_id).update(name=name,password=make_password(password))
            data={"code":1,"msg":"账户重置成功"}
        except IntegrityError as e:
            #得到异常消息
            msg=str(e)
            logger.error(msg)
            data={"code":0,"msg":msg}

        return JsonResponse(data)
        #return HttpResponse(json.dumps(data,ensure_ascii = False), "text/html")
        
#用户组
class GroupListView(AdminUserRequiredMixin,TemplateView):
    """
    显示
    """
    template_name = 'myauth/group.html'

    def get_context_data(self, **kwargs):
        context = {
            # 'app': 'Assets',
            # 'action': 'Asset list',
        }
        kwargs.update(context)
        return super(GroupListView, self).get_context_data(**kwargs)

class GroupAddView(AdminUserRequiredMixin,TemplateView):
    """
    添加
    """
    template_name = 'myauth/groupadd.html'
    model = Group

    #显示添加模板
    def get_context_data(self, **kwargs):
        context = {
            # 'app': 'Assets',
            # 'action': 'Asset list',
        }
        kwargs.update(context)
        return super(GroupAddView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        name = request.POST.get("row[name]")

        msg=""
        try:
            ormdata = self.model.objects.create(name=name)
            ormdata.save()
            data={"code":1,"msg":msg}
        except IntegrityError as e:
            #得到异常消息
            #msg=str(e.__cause__)
            msg = "用户组已经存在"
            logger.error(e.__cause__)
            data={"code":0,"msg":msg}

        return JsonResponse(data)

class GroupEditView(AdminUserRequiredMixin,TemplateView):
    """
    编辑
    """
    template_name = 'myauth/groupedit.html'
    model = Group

    def get(self, request, *args, **kwargs):
        """
        得到提交的ids
        """
        _id = request.GET.get('id')
        #根据id得到数据
        ormdata = self.model.objects.get(id=_id)
        self.id = ormdata.id
        self.name = ormdata.name

        return super(GroupEditView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):
        context = {
            'id': self.id,
            'name': self.name
        }
        kwargs.update(context)
        return super(GroupEditView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        id = request.POST.get('id')
        name = request.POST.get("row[name]")

        msg=""
        try:
            ormdata = self.model.objects.get(id=id)
            ormdata.name=name

            ormdata.save()
            data={"code":1,"msg":msg}
        except IntegrityError as e:
            #得到异常消息
            #msg=str(e.__cause__)
            msg = "用户组已经存在"
            logger.error(e.__cause__)
            data={"code":0,"msg":msg}

        return JsonResponse(data)

class GroupDelView(AdminUserRequiredMixin,TemplateView):
    """
    删除
    """
    model = Group

    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        #得到批量或者单个要删除的id
        ids = request.POST.getlist("ids[]")

        msg=""
        #批量删除，使用in方法
        self.model.objects.filter(id__in=ids).delete()
        data={"code":1,"msg":msg}

        return JsonResponse(data)


class GroupUsersAddView(AdminUserRequiredMixin,TemplateView):
    """
    添加组成员
    """
    template_name = 'myauth/groupusersadd.html'
    #model = Group

    def get(self, request, *args, **kwargs):
        """
        
        """
        self.groupid = int(request.GET.get('groupid'))

        return super(GroupUsersAddView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):
        #获取设置组信息
        group=Group.objects.get(id=self.groupid)
        #获取非管理员切激活的用户
        user_ormdata = User.objects.filter(is_active=1).filter(is_superuser=0)#.values('id', 'name', 'nickname')
        html = []
        
        for data in user_ormdata:
            groups = []
            for i in data.groups.all():
                groups.append(i.id)
            #判断当前组是否在用户所在组
            if self.groupid in groups:
                html.append('<option value="%d" selected>%s(%s)</option>' % (data.id,data.name,data.nickname))
            else:
                html.append('<option value="%d">%s(%s)</option>' % (data.id,data.name,data.nickname))

        context = {
            'id': self.groupid,
            'group': group,
            'html':"".join(html)
        }
        kwargs.update(context)
        return super(GroupUsersAddView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        _id = request.POST.get('id')
        name = request.POST.get("row[name]")
        users = request.POST.getlist("users[]")

        #未选择成员
        if users==[]:
            data={"code":0,"msg":"请选择分配组成员"}
            return JsonResponse(data)

        msg=""
        try:
            group_ormdata = Group.objects.get(id=_id)
            isdel = False
            for user in users:
                
                user_ormdata = User.objects.get(id=int(user))
                if not isdel:
                    #删除当前组下的所有用户
                    user_ormdata.groups.through.objects.filter(group_id=_id).delete()
                    isdel=True
                user_ormdata.groups.add(group_ormdata)

            # ormdata.save()
            data={"code":1,"msg":msg}
        except IntegrityError as e:
            #得到异常消息
            msg=str(e.__cause__)
            logger.error(e.__cause__)
            data={"code":0,"msg":msg}

        return JsonResponse(data)

#权限
class PermissionListView(AdminUserRequiredMixin,TemplateView):
    """
    显示
    """
    template_name = 'myauth/permission.html'

    def get_context_data(self, **kwargs):
        context = {
            # 'app': 'Assets',
            # 'action': 'Asset list',
        }
        kwargs.update(context)
        return super(PermissionListView, self).get_context_data(**kwargs)

class PermissionGroupAddView(AdminUserRequiredMixin,TemplateView):
    """
    添加
    """
    template_name = 'myauth/permissiongroupadd.html'

    def get(self, request, *args, **kwargs):

        self.groupid = int(request.GET.get('id'))

        return super(PermissionGroupAddView, self).get(request, *args, **kwargs)

    #显示添加模板
    def get_context_data(self, **kwargs):
        
        group = Group.objects.get(id=self.groupid)

        context = {
            'groupname': group.name,
            'id': self.groupid,
        }
        kwargs.update(context)
        return super(PermissionGroupAddView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        #组id
        _id = request.POST.get('id')

        #菜单id，使用,号连接
        menusid = request.POST.get("menusid")

        #未选择成员
        if menusid=="":
            data={"code":0,"msg":"请选择分配菜单权限"}
            return JsonResponse(data)

        msg=""
        try:

            isdel = False
            group_ormdata = Group.objects.get(id=_id)

            for perms in menusid.split(','):
                perms_ormdata = Menu.objects.get(id=perms)
                if not isdel:
                    #删除当前组下的所有菜单权限
                    group_ormdata.permissions.through.objects.filter(group_id=_id).delete()
                    isdel=True
                group_ormdata.permissions.add(perms_ormdata)
            data={"code":1,"msg":msg}
        except IntegrityError as e:
            #得到异常消息
            msg=str(e.__cause__)
            logger.error(e.__cause__)
            data={"code":0,"msg":msg}

        return JsonResponse(data)

class PermissionUserAddView(AdminUserRequiredMixin,TemplateView):
    """
    添加
    """
    template_name = 'myauth/permissionuseradd.html'

    def get(self, request, *args, **kwargs):

        self.id = int(request.GET.get('id'))

        return super(PermissionUserAddView, self).get(request, *args, **kwargs)

    #显示添加模板
    def get_context_data(self, **kwargs):
        
        user = User.objects.get(id=self.id)

        context = {
            'name': user.name,
            'id': self.id,
        }
        kwargs.update(context)
        return super(PermissionUserAddView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        #组id
        _id = request.POST.get('id')

        #菜单id，使用,号连接
        menusid = request.POST.get("menusid")

        #未选择成员
        if menusid=="":
            data={"code":0,"msg":"请选择分配菜单权限"}
            return JsonResponse(data)

        msg=""
        try:

            isdel = False
            user_ormdata = User.objects.get(id=_id)

            for perms in menusid.split(','):
                perms_ormdata = Menu.objects.get(id=perms)
                if not isdel:
                    #删除当前组下的所有菜单权限
                    user_ormdata.permissions.through.objects.filter(user_id=_id).delete()
                    isdel=True
                user_ormdata.permissions.add(perms_ormdata)
            data={"code":1,"msg":msg}
        except IntegrityError as e:
            #得到异常消息
            msg=str(e.__cause__)
            logger.error(e.__cause__)
            data={"code":0,"msg":msg}

        return JsonResponse(data)
