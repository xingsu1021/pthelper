from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.conf import settings
import git

# Create your views here.
#------------------------------
#class BaiDuOcrView(LoginRequiredMixin,TemplateView):
    #"""
    #百度OCR配置
    #"""
    #template_name = 'common/baidu_ocr.html'

    ##显示添加模板
    #def get(self, request, *args, **kwargs):
        #"""
        #得到
        #"""

        #return super(BaiDuOcrView, self).get(request, *args, **kwargs)

    ##显示编辑模板
    #def get_context_data(self, **kwargs):
        
        ##获取记录
        #orm_count = BaiDuOcr.objects.count()
        #if orm_count == 0:
            
            #context = {}
        #else:
            ##获取一条数据
            #ormdata = BaiDuOcr.objects.first()
            #context = {
                #'id': ormdata.id,
                #'app_id': ormdata.app_id,
                #'app_key': ormdata.app_key,
                #'secret_key': ormdata.secret_key,
            #}
        #kwargs.update(context)
        #return super(BaiDuOcrView, self).get_context_data(**kwargs)

    ##数据提交接收方法
    #def post(self, request, *args, **kwargs):
        #"""
        #数据提交
        #"""
        #_id = request.POST.get('id','')
        #app_id = request.POST.get("app_id").strip()
        #app_key = request.POST.get("app_key").strip()
        #secret_key = request.POST.get("secret_key").strip()
        
        #if _id == '':
            #ormdata = BaiDuOcr.objects.create(app_id=app_id,
                                              #app_key=app_key,
                                              #secret_key=secret_key,
                                              #)
        #else:
            #ormdata = BaiDuOcr.objects.get(id=_id)
            #ormdata.app_id = app_id
            #ormdata.app_key = app_key
            #ormdata.secret_key = secret_key

        #ormdata.save()

        #response_data={"code":1,"msg":"添加成功"}

        #return JsonResponse(response_data)
    
class BackupView(LoginRequiredMixin,TemplateView):
    """
    备份恢复
    """
    template_name = 'common/backup.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        得到
        """

        return super(BackupView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):
        
        context = {

        }
        kwargs.update(context)
        return super(BackupView, self).get_context_data(**kwargs)
    

class UpdateView(LoginRequiredMixin,TemplateView):
    """
    升级
    """
    template_name = 'common/update.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        得到
        """

        return super(UpdateView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):
        
        context = {

        }
        kwargs.update(context)
        return super(UpdateView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        action = request.POST.get('action')
        
        if action == 'update':
            #指定仓库地址
            repo = git.repo.Repo(settings.BASE_DIR)
            #通过Repo对象获取git对象
            git = repo.git
            #通过repo对象获取remote对象
            remote = repo.remote()
            remote.pull()
            
            log_msg=git.log()
            print (log_msg)


        response_data={"code":1,"msg":"添加成功"}

        return JsonResponse(response_data)