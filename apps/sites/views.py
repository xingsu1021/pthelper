from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .models import SiteConfig, SiteRank, SiteInfo, SiteProxy

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
        sign_type = request.POST.get("sign_type").strip()

        ormdata = SiteConfig.objects.create(name=name,
                                            name_cn=name_cn,
                                            index_url=index_url,
                                            sign_type = sign_type
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
            'sign_type':self.ormdata.sign_type,

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
        sign_type = request.POST.get("sign_type").strip()

        _id = request.POST.get('id')

        ormdata = SiteConfig.objects.get(id=_id)

        ormdata.name = name
        ormdata.name_cn = name_cn
        ormdata.index_url = index_url
        ormdata.sign_type = sign_type

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
        #
        status = request.POST.get("status","none")
        proxy_id = request.POST.get("proxy_id","")
        
        if status == 'on' and proxy_id == "":
            response_data={"code":0,"msg":"请选择代理"}
            return JsonResponse(response_data)

        siteconfig_name_cn = list(SiteConfig.objects.filter(name=siteconfig_name).values_list('name_cn',flat=True))
        
        if status == "none":
            #不打开代理设置
            ormdata = SiteInfo.objects.create(siteconfig_name=siteconfig_name,
                                                cookie=cookie,
                                                passkey=passkey,
                                                siteconfig_name_cn = siteconfig_name_cn[0]
                                                )
        else:
            ormdata_siteproxy = SiteProxy.objects.get(id=int(proxy_id))
            ormdata = SiteInfo.objects.create(siteconfig_name=siteconfig_name,
                                                cookie=cookie,
                                                passkey=passkey,
                                                siteconfig_name_cn = siteconfig_name_cn[0],
                                                siteproxy_id = ormdata_siteproxy
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
        
        if self.ormdata.siteproxy_id != None:
            siteproxy_id = self.ormdata.siteproxy_id.id
        else:
            siteproxy_id = ""

        context = {
            'id': self._id,
            'siteconfig_name': self.ormdata.siteconfig_name,
            'cookie': self.ormdata.cookie,
            'passkey': self.ormdata.passkey,
            'siteproxy_id': siteproxy_id,
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
        #
        status = request.POST.get("status","none")
        proxy_id = request.POST.get("proxy_id","")
        
        if status == 'on' and proxy_id == "":
            response_data={"code":0,"msg":"请选择代理"}
            return JsonResponse(response_data)
        
        _id = request.POST.get('id')

        siteconfig_name_cn = list(SiteConfig.objects.filter(name=siteconfig_name).values_list('name_cn',flat=True))
        
        ormdata = SiteInfo.objects.get(id=_id)

        ormdata.siteconfig_name = siteconfig_name
        ormdata.cookie = cookie
        ormdata.passkey = passkey
        ormdata.siteconfig_name_cn = siteconfig_name_cn[0]
        if status != "none":
            ormdata_siteproxy = SiteProxy.objects.get(id=int(proxy_id))
            ormdata.siteproxy_id = ormdata_siteproxy
        else:
            ormdata.siteproxy_id = None

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
    
#==========================================================================================
class SiteProxyListView(LoginRequiredMixin,TemplateView):
    """
    显示
    """
    template_name = 'sites/siteproxy.html'

    def get(self, request, *args, **kwargs):
        """
        
        """
        return super(SiteProxyListView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            # 'data': self.ormdata_game
        }
        kwargs.update(context)
        return super(SiteProxyListView, self).get_context_data(**kwargs)
    
    
class SiteProxyAddView(LoginRequiredMixin,TemplateView):
    """
    添加
    """
    template_name = 'sites/siteproxyadd.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        """
        return super(SiteProxyAddView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
        }
        kwargs.update(context)
        return super(SiteProxyAddView, self).get_context_data(**kwargs)


    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        name = request.POST.get("name").strip()
        address = request.POST.get("address").strip()
        ptype = request.POST.get("ptype").strip()
        port = request.POST.get("port")
        username = request.POST.get("username").strip()
        userpassword = request.POST.get("userpassword").strip()

        ormdata = SiteProxy.objects.create(name=name,
                                            address=address,
                                            ptype=ptype,
                                            port = port,
                                            username = username,
                                            userpassword = userpassword
                                            )

        ormdata.save()
        
        response_data={"code":1,"msg":"添加成功"}
        

        return JsonResponse(response_data)
    
class SiteProxyEditView(LoginRequiredMixin,TemplateView):
    """
    编辑域名
    """
    template_name = 'sites/siteproxyedit.html'

    #显示添加模板
    def get(self, request, *args, **kwargs):
        """
        得到
        """

        #记录ID
        self._id = request.GET.get('id')
        self.ormdata = SiteProxy.objects.get(id=self._id)

        return super(SiteProxyEditView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            'id': self._id,
            'name': self.ormdata.name,
            'address': self.ormdata.address,
            'ptype': self.ormdata.ptype,
            'port':self.ormdata.port,
            'username':self.ormdata.username,
            'userpassword':self.ormdata.userpassword,

        }
        kwargs.update(context)
        return super(SiteProxyEditView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        name = request.POST.get("name").strip()
        address = request.POST.get("address").strip()
        ptype = request.POST.get("ptype").strip()
        port = request.POST.get("port")
        username = request.POST.get("username").strip()
        userpassword = request.POST.get("userpassword").strip()

        _id = request.POST.get('id')

        ormdata = SiteProxy.objects.get(id=_id)

        ormdata.name = name
        ormdata.address = address
        ormdata.ptype = ptype
        ormdata.port = port
        ormdata.username = username
        ormdata.userpassword = userpassword

        ormdata.save()

        response_data={"code":1,"msg":"添加成功"}

        return JsonResponse(response_data)

class SiteProxyDelView(LoginRequiredMixin,TemplateView):
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

        SiteProxy.objects.filter(id__in=ids).delete()

        #Site.objects.filter(id=i).delete()

        response_data={"code":1,"msg":"操作成功"}


        return JsonResponse(response_data)
