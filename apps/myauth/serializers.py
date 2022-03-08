# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from rest_framework import viewsets, serializers, generics
from .models import User


# class AdminUserSerializer(serializers.ModelSerializer):
#     assets = serializers.PrimaryKeyRelatedField(many=True, queryset=Asset.objects.all())

#     class Meta:
#         model = AdminUser
#         fields = '__all__'

#     def get_field_names(self, declared_fields, info):
#         fields = super(AdminUserSerializer, self).get_field_names(declared_fields, info)
#         fields.append('assets_amount')
#         return fields


# class SystemUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SystemUser
#         exclude = ('_password', '_private_key', '_public_key')

#     def get_field_names(self, declared_fields, info):
#         fields = super(SystemUserSerializer, self).get_field_names(declared_fields, info)
#         fields.extend(['assets_amount'])
#         return fields


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'nickname', 'is_admin', 'mobile')
