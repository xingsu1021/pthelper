from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .models import Tools

# Create your views here.

class ToolsListView(LoginRequiredMixin,TemplateView):
    """
    显示
    """
    template_name = 'download/tools.html'

    def get(self, request, *args, **kwargs):
        """
        
        """
        return super(ToolsListView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            # 'data': self.ormdata_game
        }
        kwargs.update(context)
        return super(ToolsListView, self).get_context_data(**kwargs)
    
    
class ToolsAddView(LoginRequiredMixin,TemplateView):
    """
    添加
    """
    template_name = 'download/toolsadd.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        """
        return super(ToolsAddView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
        }
        kwargs.update(context)
        return super(ToolsAddView, self).get_context_data(**kwargs)


    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        name = request.POST.get("name").strip()
        url = request.POST.get("url").strip()
        typed = request.POST.get("typed").strip()
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()
        dirname = request.POST.get("dirname").strip()

        
        ormdata = Tools.objects.create(name=name,
                                        url=url,
                                        typed=typed,
                                        username=username,
                                        password=password,
                                        dirname=dirname
                                        )

        ormdata.save()
        
        response_data={"code":1,"msg":"添加成功"}
        

        return JsonResponse(response_data)
    
class ToolsEditView(LoginRequiredMixin,TemplateView):
    """
    编辑域名
    """
    template_name = 'download/toolsedit.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        得到
        """

        #记录ID
        self._id = request.GET.get('id')
        self.ormdata = Tools.objects.get(id=self._id)

        return super(ToolsEditView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            'id': self._id,
            'url': self.ormdata.url,
            'name': self.ormdata.name,
            'typed': self.ormdata.typed,
            'username': self.ormdata.username,
            'password': self.ormdata.password,
            'dirname': self.ormdata.dirname
        }
        kwargs.update(context)
        return super(ToolsEditView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        url = request.POST.get("url").strip()
        name = request.POST.get("name").strip()
        typed = request.POST.get("typed").strip()
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()
        dirname = request.POST.get("dirname").strip()

        _id = request.POST.get('id')

        ormdata = Tools.objects.get(id=_id)

        ormdata.url = url
        ormdata.name=name
        ormdata.typed = typed
        ormdata.username = username
        ormdata.password = password
        ormdata.dirname = dirname

        ormdata.save()

        response_data={"code":1,"msg":"添加成功"}

        return JsonResponse(response_data)

class ToolsDelView(LoginRequiredMixin,TemplateView):
    """
    删除
    """
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """

        #得到批量或者单个要删除的id
        ids = request.POST.getlist("ids[]")
        #print("ids====>",ids)

        Tools.objects.filter(id__in=ids).delete()

        #Site.objects.filter(id=i).delete()

        response_data={"code":1,"msg":"操作成功"}


        return JsonResponse(response_data)
    
#==================