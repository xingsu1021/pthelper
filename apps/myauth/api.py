# ~*~ coding: utf-8 ~*~

from rest_framework import viewsets, generics
from rest_framework import mixins

from .models import User
from .permissions import IsSuperUser,IsValidUser
from . import serializers

class UserListViewSet(viewsets.ModelViewSet):
    #查询所有的数据
    queryset = User.objects.all()
    #序列化(表现层,将数据按照一定格式返回给用户)
    serializer_class = serializers.UserSerializer
    #可以通过id和name来筛选。
    #API后面为?id=1，就会抽选User id=1的用户。?name=sftang会抽选用户名是sftang的用户 (需要rest client，不能直接浏览器访问)
    filter_fields = ('id', 'name')

#使用mixin实现
# class UserApi(mixins.RetrieveModelMixin,
#                   mixins.UpdateModelMixin,
#                   mixins.DestroyModelMixin,
#                   generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer
#     permission_classes = (IsSuperUser,)

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

class UserApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsSuperUser,)
