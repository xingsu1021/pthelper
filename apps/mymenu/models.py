from django.db import models

# Create your models here.
class Menu(models.Model):
    """
    菜单
    """
    name = models.CharField('菜单名', max_length=50, unique=True)
    menuurl = models.CharField('url地址', max_length=150)
    menupid = models.IntegerField(verbose_name='父ID')
    menuseq = models.IntegerField('菜单排序')
    menupath = models.CharField(verbose_name='菜单级别序号,父id,使用逗号分割', max_length=100)
    menutype = models.IntegerField('菜单类型 1、菜单 2、功能')

    #class Meta:
        #db_table = 'menu' #自定义表名称为mytable
        #unique_together=("name","menuurl")