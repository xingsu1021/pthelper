from django.shortcuts import render

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.management import call_command
import logging
import tempfile
import os
import shutil

from sites.models import SiteInfo,SiteConfig
from cron.models import Log
from common.sites_sign import signIngress

#==================
@login_required
def backupExport(request):
    """        
    备份数据
    """
    logger = logging.getLogger('django')
    
    if request.method == "POST":
        action = request.POST.get('action','')
        
        backup_file = os.path.join(settings.BACKUP_DIR,'pthelper.json')
        logger.info("Starting backup process.")
        
        with tempfile.TemporaryDirectory() as d:
            dump_path = os.path.join(d, 'dump.json')
            logger.info("Starting data dump...")
            #call_command('dumpdata', '--exclude','cron.Log',natural_foreign=True, output=dump_path)
            call_command('dumpdata', exclude=['cron.Log'], natural_foreign=True, output=dump_path)
            
            logger.info("Data dumped.")
            logger.info("Copying BACKUP_DIR to %s...", backup_file)
            #shutil.copytree(settings.MEDIA_ROOT, os.path.join(d, 'media'))
            shutil.copyfile(dump_path, backup_file)

            logger.info('Copy done.')
            #backup_path = os.path.join(settings.BACKUP_DIR, datetime.date.today().strftime("%Y-%m-%d.zip"))
            #with zipfile.ZipFile(backup_path, mode='w') as backup_zip:
                #for root, dirs, files in os.walk(d):
                    #for file in files:
                        #filepath = os.path.join(root, file)
                        #logger.info("Compressing {}...".format(filepath))
                        #backup_zip.write(filepath,
                                         #arcname=os.path.relpath(filepath, d))
                #logger.info("{} created.".format(backup_path))

        response_data={"code":0,"msg":"ok" }
    
        return JsonResponse(response_data)
    
#==================
@login_required
def backupImport(request):
    """
    数据恢复
    """
    logger = logging.getLogger('django')
    
    if request.method == "POST":
        action = request.POST.get('action','')
        
        backup_file = os.path.join(settings.BACKUP_DIR,'pthelper.json')
        logger.info("Starting load process.")    
        
        call_command('loaddata', backup_file)
        
        
#==================
@login_required
def signAgain(request):
    """
    补签
    """
    if request.method == "POST":
        action = request.POST.get('action')
        name = request.POST.get('name')
        _id = request.POST.get('id','')
        
        if action != 'again' or _id == "":
            response_data={"code":0,"msg":"未知操作" }
    
            return JsonResponse(response_data) 
        
        #获取配置的站点信息
        site_info = SiteInfo.objects.get(siteconfig_name=name)

        site_name = site_info.siteconfig_name
        site_cookie = site_info.cookie
        #获取站点配置信息
        site_config = SiteConfig.objects.get(name=site_name)
        site_url = site_config.index_url
        site_name_cn = site_config.name_cn
        site_sign_type = site_config.sign_type
     
        #统一签到入口
        flag, data = signIngress(site_name, site_name_cn, site_url, site_cookie, site_sign_type)
                
        #补签成功，刷新状态
        if flag:
            Log.objects.filter(id=_id).update(status=flag)
        
        #print(site_name,data)
        if flag:
            response_data={"code":1,"msg":data }
        else:
            response_data={"code":0,"msg":data }

        return JsonResponse(response_data)         

#==================
@login_required
def signCheck(request):
    """
    校验
    """
    if request.method == "POST":
        action = request.POST.get('action')
        _id = request.POST.get('id','')
        
        if action != 'check' or _id == "":
            response_data={"code":0,"msg":"未知操作" }
    
            return JsonResponse(response_data) 
        
        #获取配置的站点信息
        site_info = SiteInfo.objects.get(id=_id)

        site_name = site_info.siteconfig_name
        site_cookie = site_info.cookie
        #获取站点配置信息
        site_config = SiteConfig.objects.get(name=site_name)
        site_url = site_config.index_url
        site_name_cn = site_config.name_cn
        site_sign_type = site_config.sign_type
     
        #统一签到入口
        flag, data = signIngress(site_name, site_name_cn, site_url, site_cookie, site_sign_type)
        
        #print(site_name,data)
        if flag:
            response_data={"code":1,"msg":data }
        else:
            response_data={"code":0,"msg":data }

        return JsonResponse(response_data) 