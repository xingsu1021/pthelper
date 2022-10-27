from django.shortcuts import render

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.management import call_command
import logging
import tempfile
import os
from datetime import datetime
import simplejson as json

#==================
@login_required
def backupExport(request):
    """        
    备份数据
    """
    logger = logging.getLogger('django')
    
    if request.method == "POST":
        
        #backup_file = os.path.join(settings.BACKUP_DIR,'pthelper.json')
        backup_file = os.path.join(settings.BACKUP_DIR,'export_{}.json'.format(datetime.now().strftime("%Y-%m-%d_%H-%M")))
        logger.info("开始导出数据.")
        
        with tempfile.TemporaryDirectory() as d:
            dump_path = os.path.join(d, 'dump.json')
          
            #call_command('dumpdata', '--exclude','cron.Log',natural_foreign=True, output=dump_path)
            #call_command('dumpdata', exclude=['cron.Log'], natural_foreign=True, output=dump_path, format='json', indent=4)
            call_command('dumpdata', exclude=['authtoken.Token'], natural_foreign=True, natural_primary=True, output=dump_path, format='json', indent=4)
            
            logger.info("备份完成.")
            logger.info("开始转换备份文件 %s...", backup_file)
            #将乱码转换成中文
            with open(dump_path) as f:
                    data = json.load(f)
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            logger.info('转换完成.')
            #backup_path = os.path.join(settings.BACKUP_DIR, datetime.date.today().strftime("%Y-%m-%d.zip"))
            #with zipfile.ZipFile(backup_path, mode='w') as backup_zip:
                #for root, dirs, files in os.walk(d):
                    #for file in files:
                        #filepath = os.path.join(root, file)
                        #logger.info("Compressing {}...".format(filepath))
                        #backup_zip.write(filepath,
                                         #arcname=os.path.relpath(filepath, d))
                #logger.info("{} created.".format(backup_path))

        response_data={"code":1,"msg":"备份完成" }
    
        return JsonResponse(response_data)
    
#==================
@login_required
def backupImport(request):
    """
    数据恢复
    """
    
    if request.method == "POST":
        
        name = request.POST.get('name')
        backup_file = os.path.join(settings.BACKUP_DIR, name)
        try:
            
            call_command('loaddata', backup_file)
            
            response_data={"code":1,"msg":"恢复完成" }
        except Exception as e:
            response_data={"code":0,"msg":"恢复失败" + str(e) }
    
        return JsonResponse(response_data)        

#==================        
@login_required
def backupList(request):
    """        
    列出备份数据
    """
    data = {}
    data['code'] = 0
    data['msg'] = ""
    data['data'] = []    
    
    for file_name in os.listdir(settings.BACKUP_DIR):
            data['data'].append({"name":file_name,
                                 "url": "/backups/" + file_name
                                 })

    return JsonResponse(data)

#==================        
@login_required
def backupDel(request):
    """        
    删除备份数据
    """
    name = request.POST.get('name')
    backup_file = os.path.join(settings.BACKUP_DIR, name)
    try:
        
        os.remove(backup_file)
        
        response_data={"code":1,"msg":"删除成功" }
    except Exception as e:
        response_data={"code":0,"msg":"删除失败" + str(e) }

    return JsonResponse(response_data)    
    
