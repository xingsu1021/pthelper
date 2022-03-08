from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .models import SiteConfig, SiteRank, SiteInfo

# Create your views here.
class SiteConfigListView(LoginRequiredMixin,TemplateView):
    """
    显示
    """
    template_name = 'sites/siteconfig.html'

    def get(self, request, *args, **kwargs):
        """
        
        """
        return super(SiteConfigListView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            # 'data': self.ormdata_game
        }
        kwargs.update(context)
        return super(SiteConfigListView, self).get_context_data(**kwargs)
    
    
class SiteConfigAddView(LoginRequiredMixin,TemplateView):
    """
    添加
    """
    template_name = 'sites/siteconfigadd.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        """
        return super(SiteConfigAddView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
        }
        kwargs.update(context)
        return super(SiteConfigAddView, self).get_context_data(**kwargs)


    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        name = request.POST.get("name").strip()
        name_cn = request.POST.get("name_cn").strip()
        index_url = request.POST.get("index_url").strip()

        ormdata = SiteConfig.objects.create(name=name,
                                            name_cn=name_cn,
                                            index_url=index_url,
                                            )

        ormdata.save()
        
        response_data={"code":1,"msg":"添加成功"}
        

        return JsonResponse(response_data)
    
class SiteConfigEditView(LoginRequiredMixin,TemplateView):
    """
    编辑域名
    """
    template_name = 'sites/siteconfigedit.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        得到
        """

        #记录ID
        self._id = request.GET.get('id')
        self.ormdata = SiteConfig.objects.get(id=self._id)

        return super(SiteConfigEditView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            'id': self._id,
            'name': self.ormdata.name,
            'name_cn': self.ormdata.name_cn,
            'index_url': self.ormdata.index_url,

        }
        kwargs.update(context)
        return super(SiteConfigEditView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        name = request.POST.get("name").strip()
        name_cn = request.POST.get("name_cn").strip()
        index_url = request.POST.get("index_url").strip()

        _id = request.POST.get('id')

        ormdata = SiteConfig.objects.get(id=_id)

        ormdata.name = name
        ormdata.name_cn = name_cn
        ormdata.index_url = index_url

        ormdata.save()

        response_data={"code":1,"msg":"添加成功"}

        return JsonResponse(response_data)

class SiteConfigDelView(LoginRequiredMixin,TemplateView):
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

        SiteConfig.objects.filter(id__in=ids).delete()

        #Site.objects.filter(id=i).delete()

        response_data={"code":1,"msg":"操作成功"}


        return JsonResponse(response_data)
    
#==================
class SiteRankConfigListView(LoginRequiredMixin,TemplateView):
    """
    显示
    """
    template_name = 'sites/siterankconfig.html'

    def get(self, request, *args, **kwargs):
        """
        
        """
        return super(SiteRankConfigListView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            # 'data': self.ormdata_game
        }
        kwargs.update(context)
        return super(SiteRankConfigListView, self).get_context_data(**kwargs)
    
    
class SiteRankConfigAddView(LoginRequiredMixin,TemplateView):
    """
    添加
    """
    template_name = 'sites/siterankconfigadd.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        """
        return super(SiteRankConfigAddView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
        }
        kwargs.update(context)
        return super(SiteRankConfigAddView, self).get_context_data(**kwargs)


    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        name = request.POST.get("name").strip()
        siteconfig_name = request.POST.get("siteconfig_name")
        download = request.POST.get("download").strip()
        up_time = request.POST.get("up_time")
        upload = request.POST.get("upload",0)
        ratio = request.POST.get("ratio").strip()
        privilege = request.POST.get("privilege").strip()
        serial_number = request.POST.get("serial_number")

        ormdata = SiteRank.objects.create(name=name,
                                            siteconfig_name=siteconfig_name,
                                            download=download,
                                            up_time=up_time,
                                            upload=upload,
                                            ratio=ratio,
                                            privilege=privilege,
                                            serial_number=serial_number,
                                            )

        ormdata.save()
        
        response_data={"code":1,"msg":"添加成功"}
        

        return JsonResponse(response_data)
    
class SiteRankConfigEditView(LoginRequiredMixin,TemplateView):
    """
    编辑域名
    """
    template_name = 'sites/siterankconfigedit.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        得到
        """

        #记录ID
        self._id = request.GET.get('id')
        self.ormdata = SiteRank.objects.get(id=self._id)

        return super(SiteRankConfigEditView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            'id': self._id,
            'name': self.ormdata.name,
            'siteconfig_name': self.ormdata.siteconfig_name,
            'download': self.ormdata.download,
            'up_time': self.ormdata.up_time,
            'upload': self.ormdata.upload,
            'ratio': self.ormdata.ratio,
            'privilege': self.ormdata.privilege,
            'serial_number': self.ormdata.serial_number,

        }
        kwargs.update(context)
        return super(SiteRankConfigEditView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        name = request.POST.get("name").strip()
        siteconfig_name = request.POST.get("siteconfig_name")
        download = request.POST.get("download").strip()
        up_time = request.POST.get("up_time")
        upload = request.POST.get("upload",0)
        ratio = request.POST.get("ratio").strip()
        privilege = request.POST.get("privilege").strip()
        serial_number = request.POST.get("serial_number")

        _id = request.POST.get('id')

        ormdata = SiteRank.objects.get(id=_id)

        ormdata.name = name
        ormdata.siteconfig_name = siteconfig_name
        ormdata.download = download
        ormdata.up_time = up_time
        ormdata.upload = upload
        ormdata.ratio = ratio
        ormdata.privilege = privilege
        ormdata.serial_number = serial_number

        ormdata.save()

        response_data={"code":1,"msg":"添加成功"}

        return JsonResponse(response_data)

class SiteRankConfigDelView(LoginRequiredMixin,TemplateView):
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

        SiteRank.objects.filter(id__in=ids).delete()

        #Site.objects.filter(id=i).delete()

        response_data={"code":1,"msg":"操作成功"}


        return JsonResponse(response_data)
    
#==================
class SiteInfoListView(LoginRequiredMixin,TemplateView):
    """
    显示
    """
    template_name = 'sites/siteinfo.html'

    def get(self, request, *args, **kwargs):
        """
        
        """
        return super(SiteInfoListView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            # 'data': self.ormdata_game
        }
        kwargs.update(context)
        return super(SiteInfoListView, self).get_context_data(**kwargs)
    
    
class SiteInfoAddView(LoginRequiredMixin,TemplateView):
    """
    添加
    """
    template_name = 'sites/siteinfoadd.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        """
        return super(SiteInfoAddView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
        }
        kwargs.update(context)
        return super(SiteInfoAddView, self).get_context_data(**kwargs)


    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        siteconfig_name = request.POST.get("siteconfig_name").strip()
        cookie = request.POST.get("cookie").strip()
        passkey = request.POST.get("passkey").strip()

        ormdata = SiteInfo.objects.create(siteconfig_name=siteconfig_name,
                                            cookie=cookie,
                                            passkey=passkey,
                                            )

        ormdata.save()
        
        response_data={"code":1,"msg":"添加成功"}
        

        return JsonResponse(response_data)
    
class SiteInfoEditView(LoginRequiredMixin,TemplateView):
    """
    编辑域名
    """
    template_name = 'sites/siteinfoedit.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        得到
        """

        #记录ID
        self._id = request.GET.get('id')
        self.ormdata = SiteInfo.objects.get(id=self._id)

        return super(SiteInfoEditView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            'id': self._id,
            'siteconfig_name': self.ormdata.siteconfig_name,
            'cookie': self.ormdata.cookie,
            'passkey': self.ormdata.passkey,
        }
        kwargs.update(context)
        return super(SiteInfoEditView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        siteconfig_name = request.POST.get("siteconfig_name").strip()
        cookie = request.POST.get("cookie").strip()
        passkey = request.POST.get("passkey").strip()

        _id = request.POST.get('id')

        ormdata = SiteInfo.objects.get(id=_id)

        ormdata.siteconfig_name = siteconfig_name
        ormdata.cookie = cookie
        ormdata.passkey = passkey


        ormdata.save()

        response_data={"code":1,"msg":"添加成功"}

        return JsonResponse(response_data)

class SiteInfoDelView(LoginRequiredMixin,TemplateView):
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

        SiteInfo.objects.filter(id__in=ids).delete()

        #Site.objects.filter(id=i).delete()

        response_data={"code":1,"msg":"操作成功"}


        return JsonResponse(response_data)