from myauth.models import User
from django.contrib.auth.hashers import  make_password

from sites.models import SiteConfig
from cron.models import JobType
from notify.models import MailType

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
    sites_data = [{'name':'hdfans','name_cn':'红豆饭','index_url':'https://hdfans.org'},
                  {'name':'1ptba','name_cn':'壹PT吧','index_url':'https://1ptba.com'},
                  {'name':'ptchina','name_cn':'铂金学院','index_url':'https://ptchina.org'},
                  {'name':'hdchina','name_cn':'瓷器','index_url':'https://hdchina.org'},
                  {'name':'hdmayi','name_cn':'小蚂蚁','index_url':'http://hdmayi.com'},
                  {'name':'msg','name_cn':'马杀鸡','index_url':'https://pt.msg.vg'},
                  {'name':'beitai','name_cn':'备胎','index_url':'https://www.beitai.pt'},
                  {'name':'oshen','name_cn':'奥申','index_url':'http://www.oshen.win'},
                  {'name':'avgv','name_cn':'爱薇','index_url':'http://avgv.cc'},
                  {'name':'eastgame','name_cn':'吐鲁番','index_url':'https://pt.eastgame.org'},
                  {'name':'keepfrds','name_cn':'朋友','index_url':'https://pt.keepfrds.com'},
                  {'name':'tjupt','name_cn':'北洋园','index_url':'https://tjupt.org'},
                  {'name':'itzmx','name_cn':'分享站','index_url':'https://pt.itzmx.com'},
                  {'name':'greatposterwall','name_cn':'海豹','index_url':'https://greatposterwall.com'},
                  {'name':'hd','name_cn':'海带','index_url':'https://www.hd.ai'},
                  {'name':'m-team','name_cn':'馒头','index_url':'https://kp.m-team.cc'},
                  {'name':'lemonhd','name_cn':'柠檬','index_url':'https://lemonhd.org'},
                  {'name':'btschool','name_cn':'学校','index_url':'https://pt.btschool.club'},
                  {'name':'pthome','name_cn':'铂金家','index_url':'https://pthome.net'},
                  {'name':'totheglory','name_cn':'听听歌','index_url':'https://totheglory.im'},
                  {'name':'hdhome','name_cn':'家园','index_url':'https://hdhome.org'},
                  {'name':'pterclub','name_cn':'猫站','index_url':'https://pterclub.com'},
                  {'name':'ourbits','name_cn':'我堡','index_url':'https://ourbits.club'},
                  {'name':'hdsky','name_cn':'天空','index_url':'https://hdsky.me'},
                  {'name':'hares','name_cn':'白兔','index_url':'https://club.hares.top'},
                  {'name':'et8','name_cn':'他吹吹风','index_url':'https://et8.org'},
                  {'name':'audiences','name_cn':'观众','index_url':'https://audiences.me'},
                  {'name':'hdcity','name_cn':'城市','index_url':'https://hdcity.city'},
                  {'name':'open','name_cn':'皇后','index_url':'https://open.cd'},
                  {'name':'hdarea','name_cn':'高清视界','index_url':'https://www.hdarea.co'},
                  {'name':'soulvoice','name_cn':'聆音','index_url':'https://pt.soulvoice.club'},
                  {'name':'nicept','name_cn':'老师','index_url':'https://www.nicept.net'},
                  {'name':'haidan','name_cn':'海胆','index_url':'https://www.haidan.video'},
                  {'name':'3wmg','name_cn':'芒果','index_url':'https://www.3wmg.com'},
                  {'name':'discfan','name_cn':'碟粉','index_url':'https://discfan.net'},
                  {'name':'htpt','name_cn':'海棠','index_url':'https://www.htpt.cc'},
                  {'name':'hddolby','name_cn':'杜比','index_url':'https://www.hddolby.com'},
                  {'name':'hdzone','name_cn':'高清地带','index_url':'https://hdzone.me'},
                  {'name':'pttime','name_cn':'时间','index_url':'https://www.pttime.org'},
                  {'name':'hdatmos','name_cn':'阿童木','index_url':'https://hdatmos.club'},
                  {'name':'52pt','name_cn':'52PT','index_url':'https://52pt.site'},
                  {'name':'hdtime','name_cn':'高清时间','index_url':'https://hdtime.org'},
                  {'name':'asf','name_cn':'A-SOUL','index_url':'https://p2p.bbs.asf.ink'},
                  ]
    
    for site in sites_data:
        get_site = SiteConfig.objects.filter(name=site['name']).count()
        if get_site == 0:
            SiteConfig.objects.create(name = site['name'],
                                      name_cn = site['name_cn'],
                                      index_url = site['index_url'],
                                      )
            print('添加站点 [%s] 成功' % site['name'])
        else:
            #更新站点配置
            #SiteConfig.objects.filter(name=site['name']).update(name_cn = site['name_cn'],
                                                                #index_url=site['index_url'],
                                                                #)
            #print('站点 [%s] 更新成功' % site['name'])
            print('站点 [%s] 已经存在,忽略...' % site['name'])
            
        
    print('开始初始化任务类型...')
    jobtypes_data = [{'name':'签到','type_id':1000},
                     {'name':'辅种','type_id':1001},
                     {'name':'刷流','type_id':1002},
                     ]
    
    for jobtype in jobtypes_data:
        get_jobtype = JobType.objects.filter(name=jobtype['name']).count()
        if get_jobtype == 0:
            JobType.objects.create(name = jobtype['name'],
                                   type_id = jobtype['type_id'],
                                   )
            print('添加任务类型 [%s] 成功' % jobtype['name'])
        else:
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
            
    print('初始化成功.')
    