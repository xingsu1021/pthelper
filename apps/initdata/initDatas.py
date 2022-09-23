from myauth.models import User
from django.contrib.auth.hashers import  make_password

from sites.models import SiteConfig, SiteInfo
from cron.models import JobType
from notify.models import MailType
from rss.models import FilmCategory, FilmType

def init_datas():
    """
    初始化数据库
    """
    print('开始初始化用户数据库...')

    if User.objects.count() == 0:
        #添加管理员
        User.objects.create(name='admin',
                            nickname='admin',
                            email = 'admin@admin.com',
                            password = make_password('123456'),
                            mobile='13911111111',
                            is_superuser=True,
                            is_active=True                            
                            )
        print('初始化管理员成功.')
    else:
        print("管理员已经存在,忽略...")

    print('开始初始化站点配置...')
    sites_data = [{'name':'hdfans','name_cn':'红豆饭','index_url':'https://hdfans.org','sign_type':'general'},
                  {'name':'1ptba','name_cn':'壹PT吧','index_url':'https://1ptba.com','sign_type':'general'},
                  {'name':'ptchina','name_cn':'铂金学院','index_url':'https://ptchina.org','sign_type':'general'},
                  {'name':'hdchina','name_cn':'瓷器','index_url':'https://hdchina.org','sign_type':'hdchina'},
                  {'name':'hdmayi','name_cn':'小蚂蚁','index_url':'http://hdmayi.com','sign_type':'general'},
                  {'name':'msg','name_cn':'马杀鸡','index_url':'https://pt.msg.vg','sign_type':'nosign'},
                  {'name':'beitai','name_cn':'备胎','index_url':'https://www.beitai.pt','sign_type':'nosign'},
                  {'name':'oshen','name_cn':'奥申','index_url':'http://www.oshen.win','sign_type':'nosign'},
                  {'name':'avgv','name_cn':'爱薇','index_url':'http://avgv.cc','sign_type':'nosign'},
                  {'name':'eastgame','name_cn':'吐鲁番','index_url':'https://pt.eastgame.org','sign_type':'nosign'},
                  {'name':'keepfrds','name_cn':'朋友','index_url':'https://pt.keepfrds.com','sign_type':'keepfrds'},
                  {'name':'tjupt','name_cn':'北洋园','index_url':'https://tjupt.org','sign_type':'tjupt'},
                  {'name':'itzmx','name_cn':'分享站','index_url':'https://pt.itzmx.com','sign_type':'nosign'},
                  {'name':'greatposterwall','name_cn':'海豹','index_url':'https://greatposterwall.com','sign_type':'nosign'},
                  {'name':'hd','name_cn':'海带','index_url':'https://www.hd.ai','sign_type':'hd'},
                  {'name':'m-team','name_cn':'馒头','index_url':'https://kp.m-team.cc','sign_type':'nosign'},
                  {'name':'lemonhd','name_cn':'柠檬','index_url':'https://lemonhd.org','sign_type':'general'},
                  {'name':'btschool','name_cn':'学校','index_url':'https://pt.btschool.club','sign_type':'btschool'},
                  {'name':'pthome','name_cn':'铂金家','index_url':'https://pthome.net','sign_type':'general'},
                  {'name':'totheglory','name_cn':'听听歌','index_url':'https://totheglory.im','sign_type':'ttg'},
                  {'name':'hdhome','name_cn':'家园','index_url':'https://hdhome.org','sign_type':'general'},
                  {'name':'pterclub','name_cn':'猫站','index_url':'https://pterclub.com','sign_type':'pterclub'},
                  {'name':'ourbits','name_cn':'我堡','index_url':'https://ourbits.club','sign_type':'general'},
                  {'name':'hdsky','name_cn':'天空','index_url':'https://hdsky.me','sign_type':'hdsky'},
                  {'name':'hares','name_cn':'白兔','index_url':'https://club.hares.top','sign_type':'hares'},
                  {'name':'et8','name_cn':'他吹吹风','index_url':'https://et8.org','sign_type':'nosign'},
                  {'name':'audiences','name_cn':'观众','index_url':'https://audiences.me','sign_type':'general'},
                  {'name':'hdcity','name_cn':'城市','index_url':'https://hdcity.city','sign_type':'hdcity'},
                  {'name':'open','name_cn':'皇后','index_url':'https://open.cd','sign_type':'opencd'},
                  {'name':'hdarea','name_cn':'高清视界','index_url':'https://www.hdarea.co','sign_type':'hdarea'},
                  {'name':'soulvoice','name_cn':'聆音','index_url':'https://pt.soulvoice.club','sign_type':'general'},
                  {'name':'nicept','name_cn':'老师','index_url':'https://www.nicept.net','sign_type':'general'},
                  {'name':'haidan','name_cn':'海胆','index_url':'https://www.haidan.video','sign_type':'haidan'},
                  {'name':'3wmg','name_cn':'芒果','index_url':'https://www.3wmg.com','sign_type':'general'},
                  {'name':'discfan','name_cn':'碟粉','index_url':'https://discfan.net','sign_type':'general'},
                  {'name':'htpt','name_cn':'海棠','index_url':'https://www.htpt.cc','sign_type':'general'},
                  {'name':'hddolby','name_cn':'杜比','index_url':'https://www.hddolby.com','sign_type':'general'},
                  {'name':'hdzone','name_cn':'高清地带','index_url':'https://hdzone.me','sign_type':'general'},
                  {'name':'pttime','name_cn':'时间','index_url':'https://www.pttime.org','sign_type':'general'},
                  {'name':'hdatmos','name_cn':'阿童木','index_url':'https://hdatmos.club','sign_type':'general'},
                  {'name':'52pt','name_cn':'52PT','index_url':'https://52pt.site','sign_type':'pt52'},
                  {'name':'hdtime','name_cn':'高清时间','index_url':'https://hdtime.org','sign_type':'general'},
                  {'name':'asf','name_cn':'A-SOUL','index_url':'https://pt.asf.ink','sign_type':'general'},
                  {'name':'ptsbao','name_cn':'烧包','index_url':'https://ptsbao.club','sign_type':'nosign'},
                  {'name':'ssd','name_cn':'春天','index_url':'https://springsunday.net','sign_type':'nosign'},
                  {'name':'gainbound','name_cn':'丐帮','index_url':'https://gainbound.net','sign_type':'general'},
                  {'name':'joyhd','name_cn':'开心','index_url':'https://www.joyhd.net','sign_type':'nosign'},
                  {'name':'carpt','name_cn':'车PT','index_url':'https://carpt.net','sign_type':'general'},
                  {'name':'piggo','name_cn':'猪猪网','index_url':'https://piggo.me','sign_type':'general'},
                  {'name':'wintersakura','name_cn':'冬樱','index_url':'https://wintersakura.net','sign_type':'general'},
                  {'name':'hdpt','name_cn':'明教','index_url':'https://hdpt.xyz','sign_type':'general'},                  
                  {'name':'u2','name_cn':'动漫花园','index_url':'https://u2.dmhy.org','sign_type':'u2'},
                  {'name':'azusa','name_cn':'梓喵','index_url':'https://azusa.ru','sign_type':'general'},
                  {'name':'kamept','name_cn':'KamePT','index_url':'https://kamept.com','sign_type':'general'},
                  {'name':'hhanclub','name_cn':'憨憨PT','index_url':'https://hhanclub.top','sign_type':'general'},
                  ]

    for site in sites_data:
        get_site = SiteConfig.objects.filter(name=site['name']).count()
        if get_site == 0:
            SiteConfig.objects.create(name = site['name'],
                                      name_cn = site['name_cn'],
                                      index_url = site['index_url'],
                                      sign_type = site['sign_type'],
                                      )
            print('添加站点 [%s] 成功' % site['name'])
        #else:
            ##更新站点配置
            #SiteConfig.objects.filter(name=site['name']).update(sign_type = site['sign_type'])

            #print('站点 [%s] 更新成功' % site['name'])
            ##print('站点 [%s] 已经存在,忽略...' % site['name'])
    #更新站点签到类型
    SiteConfig.objects.filter(name='keepfrds').update(sign_type = 'nosign')
    SiteConfig.objects.filter(name='ptsbao').update(sign_type = 'nosign')

    print('开始修复站点信息中文名称...')
    ormdata_siteinfo = SiteInfo.objects.filter(siteconfig_name_cn='')
    for siteinfo in ormdata_siteinfo:
        
        siteconfig_name_cn = list(SiteConfig.objects.filter(name=siteinfo.siteconfig_name).values_list('name_cn',flat=True))
        SiteInfo.objects.filter(siteconfig_name=siteinfo.siteconfig_name).update(siteconfig_name_cn = siteconfig_name_cn[0])


    print('开始初始化任务类型...')
    jobtypes_data = [{'name':'签到','type_id':1000},
                     {'name':'用户信息','type_id':1001},
                     {'name':'RSS订阅','type_id':1002},
                     {'name':'签到重试','type_id':1003},
                     ]

    for jobtype in jobtypes_data:
        get_jobtype = JobType.objects.filter(name=jobtype['name']).count()
        if get_jobtype == 0:
            JobType.objects.create(name = jobtype['name'],
                                   type_id = jobtype['type_id'],
                                   )
            print('添加任务类型 [%s] 成功' % jobtype['name'])
        else:
            #将原刷流更新为RSS订阅
            JobType.objects.filter(type_id=1002).update(name = 'RSS订阅')
            #将原铺种更新为用户信息
            JobType.objects.filter(type_id=1001).update(name = '用户信息')
            print('任务类型 [%s] 已经存在,忽略...' % jobtype['name'])

    print('开始初始化通知邮箱类型...')
    mailtypes_data = [{'name':'QQ邮箱','alias_name':'qq','smtp_server':'smtp.qq.com','smtp_port':465},
                      {'name':'新浪邮箱(非vip)','alias_name':'sina','smtp_server':'smtp.sina.com','smtp_port':465},
                      {'name':'网易163邮箱','alias_name':'163','smtp_server':'smtp.163.com','smtp_port':465},
                     ]

    for mailtype in mailtypes_data:
        get_mailtype = MailType.objects.filter(name=mailtype['name']).count()
        if get_mailtype == 0:
            MailType.objects.create(name = mailtype['name'],
                                    alias_name = mailtype['alias_name'],
                                    smtp_server = mailtype['smtp_server'],
                                    smtp_port = mailtype['smtp_port'],
                                    )
            print('添加邮箱类型 [%s] 成功' % mailtype['name'])
        else:
            print('邮箱类型 [%s] 已经存在,忽略...' % mailtype['name'])

    filmcategorys_data = [{'name_en':'Movies','name_cn':'电影'},
                          {'name_en':'TV Series','name_cn':'电视剧'},
                     {'name_en':'Docs','name_cn':'纪录片'},
                     {'name_en':'Animations','name_cn':'动画片'},
                     {'name_en':'TV Shows','name_cn':'综艺'},
                     {'name_en':'Sports','name_cn':'体育'},
                     {'name_en':'MV','name_cn':'音乐视频'},
                     {'name_en':'Music','name_cn':'音乐'},
                     {'name_en':'Others','name_cn':'其他'},
                     ]
    for film_category in filmcategorys_data:
        get_film_category = FilmCategory.objects.filter(name_en=film_category['name_en']).count()
        if get_film_category == 0:
            FilmCategory.objects.create(name_en = film_category['name_en'],
                                        name_cn = film_category['name_cn']
                                        )
            print('添加影视类别 [%s] 成功' % film_category['name_en'])
        else:
            print('影视类别 [%s] 已经存在,忽略...' % film_category['name_en'])

    filmtype_data = [{'name':'喜剧'},
                     {'name':'爱情'},
                 {'name':'动作'},
                 {'name':'科幻'},
                 {'name':'动画'},
                 {'name':'悬疑'},
                 {'name':'犯罪'},
                 {'name':'惊悚'},
                 {'name':'冒险'},
                 {'name':'音乐'},
                 {'name':'历史'},
                 {'name':'奇幻'},
                 {'name':'恐怖'},
                 {'name':'战争'},
                 {'name':'传记'},
                 {'name':'歌舞'},
                 {'name':'武侠'},
                 {'name':'情色'},
                 {'name':'灾难'},
                 {'name':'西部'},
                 {'name':'纪录片'},
                 {'name':'短片'},
                 {'name':'真人秀'},
                 {'name':'脱口秀'},
                 {'name':'古装'},
                 {'name':'家庭'},
                 {'name':'剧情'},
                 ]

    for film_type in filmtype_data:
        get_film_type = FilmType.objects.filter(name=film_type['name']).count()
        if get_film_type == 0:
            FilmType.objects.create(name = film_type['name'])
            print('添加影视类型 [%s] 成功' % film_type['name'])
        else:
            print('影视类型 [%s] 已经存在,忽略...' % film_type['name'])    

    print('初始化成功.')
