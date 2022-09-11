from django.db import models

# Create your models here.

class Tools(models.Model):
    """下载器"""
    name = models.CharField('下载器名称', max_length=30, unique=True)
    typed = models.CharField('下载器类型tr,qb', max_length=30)
    url = models.URLField('下载器地址', blank=True)
    username = models.CharField('下载器用户名', max_length=50)
    password = models.CharField('下载器密码', max_length=128)
    dirname = models.CharField('默认下载目录', max_length=150, null=True)