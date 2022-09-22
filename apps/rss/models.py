from django.db import models
from sites.models import SiteInfo
from download.models import Tools
from cron.models import Job
# Create your models here.

class FilmCategory(models.Model):
    """影视类别"""
    name_en = models.CharField('英文名', max_length=20)
    name_cn = models.CharField('中文名', max_length=20)

class FilmType(models.Model):
    """影视类型"""
    name = models.CharField('名称', max_length=20)

#class FilmActor(models.Model):
    #"""影视演员"""
    #name = models.CharField('名称', max_length=50)
    #name_en = models.CharField('英文名称', max_length=100)
    #constellation = models.CharField('星座', max_length=10)
    #gender = models.CharField('性别', max_length=2)
    #birth = models.DateField('出生日期')
    #birthplace = models.CharField('出生地', max_length=50)
    #job = models.CharField('职业', max_length=100)
    #description = models.TextField('简介')
    #avatar = models.URLField('头像', blank=True)
    
class Config(models.Model):
    """RSS配置"""
    name = models.CharField('自定义配置名称', max_length=50, null=True)
    url = models.URLField('RSS地址', blank=True, max_length=350, unique=True)
    #site_name = models.CharField('网站名简称,英文', max_length=50, unique=True)
    #site_name_cn = models.CharField('网站名简称,中文', max_length=50, unique=True)
    #on_update 和 on_delete 后面可以跟的词语有四个
    #1. no action 表示 不做任何操作，
    #2. set null 表示在外键表中将相应字段设置为null
    #3. set default 表示设置为默认值
    #4. cascade 表示级联操作，就是说，如果主键表中被参考字段更新，外键表中也更新，主键表中的记录被删除，外键表中改行也相应删除    
    siteinfo_id = models.ForeignKey(SiteInfo, on_delete=models.CASCADE, related_name='siteinfo')
    
class Rule(models.Model):
    """RSS规则"""
    name = models.CharField('规则名称', max_length=50, unique=True)
    config_id = models.ForeignKey(Config, on_delete=models.CASCADE, related_name='config')
    keyword = models.CharField('关键字,使用逗号分隔', max_length=100, null=True)
    tools_id = models.ForeignKey(Tools, on_delete=models.CASCADE, related_name='tools')
    status = models.BooleanField("状态启用，禁用",default=False)
    refresh_time = models.IntegerField('刷新间隔分钟', default=5)
    rate = models.CharField('码率:all,1080,2060', max_length=10, default='all')
    is_paused = models.BooleanField("是否立刻下载",default=False)
    
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job', null=True)
    
class SeedInfo(models.Model):
    """种子信息"""
    seed_name = models.CharField('种子名称', max_length=500)
    seed_type = models.CharField('种子类型', max_length=50)
    seed_details_link = models.URLField('种子详情地址', blank=True)
    seed_published_time = models.DateTimeField('发布时间')
    seed_hash_id = models.CharField('种子hash值', max_length=50)
    seed_donwload_link = models.URLField('种子下载地址', blank=True)
    seed_file_size = models.BigIntegerField('种子文件大小')
    seed_status = models.BooleanField('状态：下载，未下载', default=False)
    seed_torrent_id = models.IntegerField("在下载器的标识ID", null=True)

    photos = models.URLField('海报', blank=True)
    douban_link = models.URLField('豆瓣电影地址', blank=True)
    imdb_link = models.URLField('IMDB电影地址', blank=True)
    
    siteinfo_id = models.ForeignKey(SiteInfo, on_delete=models.CASCADE)
    rule_id = models.ForeignKey(Rule, on_delete=models.CASCADE, null=True)
    
    class Meta:
        unique_together=("seed_hash_id", "siteinfo_id")    
    