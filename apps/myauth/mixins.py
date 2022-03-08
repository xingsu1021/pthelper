# ~*~ coding: utf-8 ~*~

from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.contrib.auth.views import redirect_to_login
from mymenu.models import Menu
from myauth.models import Group

class AdminUserRequiredMixin(UserPassesTestMixin):
    """验证用户是否管理员,非管理员返回403"""
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        elif not self.request.user.is_superuser:
            self.raise_exception = True
            return False
        return True

class LoginPermissionsMixin(PermissionRequiredMixin):
    """登录、权限验证"""

    def has_permission(self):
        """
        Override this method to customize the way permissions are checked.
        """
        #得到登录用户对象
        user = self.request.user
        #管理员不检查权限
        if user.is_active and user.is_superuser:
            return True

        #得到请求的访问url
        visit_url = self.request.path
        #得到访问url的id，返回[{'id':1}]
        menuId = Menu.objects.filter(menuurl=visit_url).values('id')[0]['id']

        #检查用户权限 得到用户所拥有的菜单id list
        menus = user.get_permissions(user)


        #标识 没有权限
        no_permission = True
        if menuId in menus:
            #访问的url在权限中
            return True
        else:
            #检查组权限
            #得到用户所在的所有组ID
            usergroups = [p.id for p in user.groups.all()]
            for g in usergroups:
                #得到组对象
                group = Group.objects.get(id=g)
                #得到组对应的权限
                menus = group.get_permissions()
                if menuId in menus:
                    return True

            return False

    def dispatch(self, request, *args, **kwargs):
        #验证用户是否登录
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(),
                                     self.get_login_url(), self.get_redirect_field_name())
        
        if not self.has_permission():
            # We could also use "return self.handle_no_permission()" here
            #raise PermissionDenied(self.get_permission_denied_message())
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)
        #return super(LoginPermissionsMixin, self).dispatch(request, *args, **kwargs)