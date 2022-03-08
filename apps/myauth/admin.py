#coding: utf-8

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from myauth.models import User

# 新增用户表单
class UserCreateForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('name', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# 修改用户表单
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = "__all__"

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

# 注册用户
class MyUserAdmin(UserAdmin):

    form = UserChangeForm
    add_form = UserCreateForm

    list_display = ('name', 'created_at', 'email', 'is_delete', 'is_superuser')
    search_fields = ('name', 'email')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password', 'avatar',)}),
        ('Permissions', {'fields': ('is_delete', 'is_superuser', 'is_active')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('name', 'email', 'password1', 'password2'),
            }
        ),
    )
    ordering = ('created_at',)
    filter_horizontal = ()


admin.site.register(User, MyUserAdmin)