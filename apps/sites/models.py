from django.db import models

# Create your models here.
class SiteConfig(models.Model):
    """
    站点配置信息
    """
    name = models.CharField('网站名简称,英文', max_length=50, unique=True)
    name_cn = models.CharField('网站名简称,中文', max_length=50, unique=True)
    index_url = models.CharField('首页地址', max_length=200, unique=True)
    torrent_url = models.CharField('种子地址', max_length=200)
    bonus_url = models.CharField('魔力地址', max_length=200)
    sign_type = models.CharField('签到类型,统一签到少改代码', max_length=20, null=True)

    #class Meta:
        ##db_table = 'menu' #自定义表名称为mytable
        #unique_together=("name","name_cn","index_url")
        
class SiteRank(models.Model):
    """
    站点军衔,升级信息
    """
    name= models.CharField('级别名称', max_length=50)
    siteconfig_name = models.CharField('网站名简称,英文', max_length=50)
    download = models.CharField('下载量', max_length=50)
    up_time = models.IntegerField('升级时间,单位周')
    upload = models.CharField('上传量', max_length=50)
    ratio = models.CharField('分享率', max_length=20)
    privilege = models.CharField('信息说明', max_length=200)
    serial_number = models.IntegerField('排序序号')
    
    class Meta:
        unique_together=("name","siteconfig_name")
        
class SiteInfo(models.Model):
    """
    站点信息
    """
    siteconfig_name = models.CharField('网站名简称,英文', max_length=50, unique=True)
    siteconfig_name_cn = models.CharField('网站名简称,中文', max_length=50, null=True)
    cookie = models.CharField("网站cookie信息", max_length=1500)
    passkey = models.CharField("网站秘钥", max_length=200)
    
class SiteUser(models.Model):
    """
    站点用户信息
    """
    siteinfo_id = models.ForeignKey(SiteInfo, on_delete=models.CASCADE)
    username= models.CharField('用户名', max_length=50)
    uid = models.IntegerField('用户ID号')
    invite = models.IntegerField('邀请数量',default=0)
    create_time = models.DateTimeField('账号创建时间')
    ratio = models.CharField('分享率', max_length=20)
    upload = models.CharField('上传量', max_length=50)
    download = models.CharField('下载量', max_length=50)
    bonus = models.CharField('魔力值', max_length=50)
    score = models.CharField('积分', max_length=50)
    level = models.CharField('等级', max_length=20)
    published_seed_num = models.IntegerField('发种数量')
    seed_num = models.IntegerField('做种数量')
    totle_seed_size = models.CharField('做种体积', max_length=20,default=0)
