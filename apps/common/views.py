from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.conf import settings
from git.repo import Repo

    
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
            try:
                
                #指定仓库地址
                repo = Repo(settings.BASE_DIR)
                #通过Repo对象获取git对象
                git = repo.git
                #通过repo对象获取remote对象
                remote = repo.remote()
                remote.pull()
                
                #log_msg=git.log()
                #print (log_msg)
    
    
                response_data={"code":1,"msg":"更新成功"}
            except:
                
                response_data={"code":0,"msg":"更新失败,请查看日志"}
                
            return JsonResponse(response_data)