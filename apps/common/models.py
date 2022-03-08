from django.db import models

# Create your models here.
#class BaiDuOcr(models.Model):
    #"""
    #百度OCR信息
    #"""
    #app_id = models.CharField('APP_ID', max_length=50, unique=True)
    #app_key = models.CharField('API_KEY', max_length=50, unique=True)
    #secret_key = models.CharField('SECRET_KEY', max_length=50, unique=True)
    
class BackupInfo(models.Model):
    """
    备份信息
    """
    name = models.CharField('文件名', max_length=50,db_index = True)
    url = models.CharField('备份下载地址', max_length=200,)
    created_at = models.DateTimeField('创建时间', auto_now_add=True,db_index = True)