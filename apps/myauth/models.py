from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
# Create your models here.
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib import auth
from django.core.exceptions import PermissionDenied

from rest_framework.authtoken.models import Token

from mymenu.models import Menu

def update_last_login(sender, user, **kwargs):
    """
    A signal receiver which updates the last_login date for
    the user logging in.
    """
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])

class GroupManager(models.Manager):
    """
    The manager for the auth's Group model.
    """
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class Group(models.Model):
    """
    Groups are a generic way of categorizing users to apply permissions, or
    some other label, to those users. A user can belong to any number of
    groups.

    A user in a group automatically has all the permissions granted to that
    group. For example, if the group 'Site editors' has the permission
    can_edit_home_page, any user in that group will have that permission.

    Beyond permissions, groups are a convenient way to categorize users to
    apply some label, or extended functionality, to them. For example, you
    could create a group 'Special users', and you could write code that would
    do special things to those users -- such as giving them access to a
    members-only portion of your site, or sending them members-only email
    messages.
    """
    name = models.CharField(_('name'), max_length=80, unique=True)
    permissions = models.ManyToManyField(
        Menu,
        verbose_name=_('permissions'),
        blank=True,
    )
    tag = models.CharField('用于业务识别标签', max_length=30, default='unknow')

    objects = GroupManager()

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

    def get_permissions(self):
        """返回菜单id的list"""
        return [p.id for p in self.permissions.all()]

    def get_permissions_name(self):
        """返回菜单名称"""
        return ",".join([p.name for p in self.permissions.all()])

# A few helper functions for common logic between User and AnonymousUser.
def _user_get_all_permissions(user, obj):
    permissions = set()
    for backend in auth.get_backends():
        if hasattr(backend, "get_all_permissions"):
            permissions.update(backend.get_all_permissions(user, obj))
    return permissions


def _user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False


def _user_has_module_perms(user, app_label):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_module_perms'):
            continue
        try:
            if backend.has_module_perms(user, app_label):
                return True
        except PermissionDenied:
            return False
    return False


class PermissionsMixin(models.Model):
    """
    Add the fields and methods necessary to support the Group and Permission
    models using the ModelBackend.
    """
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )
    permissions = models.ManyToManyField(
        Menu,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True

    def get_group_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their
        groups. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                permissions.update(backend.get_group_permissions(self, obj))
        return permissions

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use simlar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    def get_permissions(self, obj=None):
        """返回菜单id的list"""
        return [p.id for p in obj.permissions.all()]

    def get_permissions_name(self, obj=None):
        """返回菜单名称"""
        return ",".join([p.name for p in obj.permissions.all()])


class UserManager(BaseUserManager):

    def create_user(self, name, email, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name=name,
            email=UserManager.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None):

        user = self.create_user(name, email, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''用户表'''

    name = models.CharField('用户名', max_length=30, unique=True)
    nickname = models.CharField('真实姓名', max_length=30)
    email = models.EmailField('邮箱', max_length=40, unique=True)
    #password = models.CharField('密码', max_length=128)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    #last_login = models.DateTimeField('最后登录时间',null=True )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    #avatar = models.FileField('头像', max_length=256, null=True, upload_to='avatars')
    avatar = models.URLField('头像', blank=True)
    mobile = models.CharField('移动电话', max_length=15, null=True)

    objects = UserManager()
    #设置认证标识，设置成标识的字段 unique=True
    USERNAME_FIELD = 'name'
    #当通过createsuperuser管理命令创建一个用户时，用于提示的一个字段名称列表
    REQUIRED_FIELDS = ('email',)

    class Meta:
        ordering = ('created_at',)

    def __unicode__(self):
        return self.name

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

# 为每个用户添加token验证
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """创建用户的时候自动创建token"""
    if created:
        Token.objects.create(user=instance)