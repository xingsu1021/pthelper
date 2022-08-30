from django.db import models

# Create your models here.
class JobType(models.Model):
    """
    任务类型
    """
    name = models.CharField('名称', max_length=20, unique=True)
    type_id = models.IntegerField("类型ID", unique=True)
    
    
class Job(models.Model):
    """
    任务
    """
    name = models.CharField('任务名称', max_length=30, unique=True)
    jobtype_id = models.IntegerField("类型ID,签到任务只允许配置一个")
    crontab_time_type = models.CharField('执行周期类型,秒,分,时,天,周,月',max_length=10)
    crontab_time = models.CharField('执行周期,* * * * *',max_length=100,null=True)
    crontab_id = models.CharField('执行ID',max_length=64)
    crontab_status = models.BooleanField('任务状态,运行,禁用',default=True)
    week = models.CharField('周', max_length=50, default="*")
    day = models.CharField('天', max_length=50, default="*")
    hour = models.CharField('时', max_length=50, default="*")
    minute = models.CharField('分', max_length=50, default="*")
    second = models.CharField('秒', max_length=50, default="*")
    sites = models.CharField('站点,使用,号分割',max_length=800,null=True)
    notifys = models.CharField('通知类型,使用,号分割',max_length=100,null=True)
    
    
class Log(models.Model):
    """
    任务日志
    """
    name = models.CharField('任务名称', max_length=20)
    type_id = models.IntegerField("类型ID")
    crontab_id = models.CharField('执行ID',max_length=64)
    site_name = models.CharField('站点名称', max_length=50,null=True)
    message = models.CharField('日志记录',max_length=300)
    created_at = models.DateTimeField('创建时间', auto_now_add=True,db_index = True)
    status = models.BooleanField('是否执行成功',default=True)