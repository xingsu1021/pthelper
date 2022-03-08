from django.db import models

# Create your models here.

    
class MailType(models.Model):    
    name = models.CharField('类型名称,QQ邮箱', max_length=20, unique=True)
    alias_name = models.CharField("类型别名,qq,sina,163", max_length=20)   
    smtp_server = models.CharField("发信地址", max_length=100)
    smtp_port = models.IntegerField("发信端口",default=465)
    
class NotifyConfig(models.Model):
    """
    通知配置
    """
    name = models.CharField('名称,特定:iyuu,telegram,email', max_length=20, unique=True)
    iyuu_key = models.CharField("IYUU令牌", max_length=200)
    tg_chat_id = models.BigIntegerField('频道ID或自身id',default=0)
    tg_token = models.CharField("telegram令牌", max_length=200)
    mail_type = models.CharField("发件邮箱类型:qq,sina,163", max_length=10,null=True)
    smtp_user = models.CharField("发信账号", max_length=100)
    smtp_password = models.CharField("发信账号密码", max_length=128)
    receive_user = models.CharField("接收账号,默认为发信账号", max_length=100)