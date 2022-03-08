from django.views.generic import TemplateView
from django.http import JsonResponse
#from django.db import IntegrityError
from django.db.utils import IntegrityError
from .models import Menu
from myauth.mixins import AdminUserRequiredMixin
from common.utils import get_logger

logger = get_logger("view")

class MenuListView(AdminUserRequiredMixin,TemplateView):
    """
    显示
    """
    template_name = 'mymenu/mymenu.html'

    def get(self, request, *args, **kwargs):
        """
        得到提交的id
        """

        return super(MenuListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            #'gameid': self.gameid,
            # 'action': 'Asset list',
        }
        kwargs.update(context)
        return super(MenuListView, self).get_context_data(**kwargs)

class MenuAddView(AdminUserRequiredMixin,TemplateView):
    """
    添加
    """
    template_name = 'mymenu/mymenuadd.html'
    model = Menu

    def get(self, request, *args, **kwargs):
        """
        得到提交的id
        """
        return super(MenuAddView, self).get(request, *args, **kwargs)

    #显示添加模板
    def get_context_data(self, **kwargs):
        #查询非功能的菜单
        menu = self.model.objects.filter(menutype=1)
        self.html_menu = []
        for data in menu:
            line = '<option value="%s">%s</option>' % (str(data.id), data.name)
            self.html_menu.append(line)

        context = {
            'html_menu': self.html_menu,
        }
        kwargs.update(context)
        return super(MenuAddView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """

        name = request.POST.get("row[name]")
        menuurl = request.POST.get("row[menuurl]")
        menutype = request.POST.get("row[menutype]")
        menuseq = request.POST.get("row[menuseq]")
        menupid = request.POST.get("row[menupid]")

        msg=""
        if name == "":
            data={"code":0,"msg":"菜单名称不能为空"}
            return JsonResponse(data)

        if menuurl == "":
            data={"code":0,"msg":"菜单地址不能为空"}
            return JsonResponse(data)

        if int(menupid) == 0:
            menupath = menupid
        else:
            #得到父菜单信息
            Pmenu = Menu.objects.get(id=menupid)
            menupath = Pmenu.menupath + ',' + menupid

        try:
            ormdata = self.model.objects.create(name=name,
                                                menuurl=menuurl,
                                                menutype=menutype,
                                                menuseq=menuseq,
                                                menupid=menupid,
                                                menupath=menupath
                                    )
            ormdata.save()
            data={"code":1,"msg":msg}
        except IntegrityError as e:
            #得到异常消息
            msg=str(e.__cause__)
            logger.error(e.__cause__)
            data={"code":0,"msg":msg}

        return JsonResponse(data)

class MenuEditView(AdminUserRequiredMixin,TemplateView):
    """
    编辑
    """
    template_name = 'mymenu/mymenuedit.html'
    model = Menu

    def get(self, request, *args, **kwargs):
        """
        得到提交的ids
        """
        self.id = request.GET.get('id')
        #根据id得到数据
        self.ormdata = self.model.objects.get(id=self.id)
        return super(MenuEditView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        #查询非功能的菜单
        menu = self.model.objects.filter(menutype=1)
        context = {
            'id': self.id,
            'mymenu': self.ormdata,
            'menu':menu
        }
        kwargs.update(context)
        return super(MenuEditView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        _id = request.POST.get('id')
        name = request.POST.get("row[name]")
        menuurl = request.POST.get("row[menuurl]")
        menutype = request.POST.get("row[menutype]")
        menuseq = request.POST.get("row[menuseq]")
        menupid = request.POST.get("row[menupid]")

        if name == "":
            data={"code":0,"msg":"菜单名称不能为空"}
            return JsonResponse(data)

        if menuurl == "":
            data={"code":0,"msg":"菜单地址不能为空"}
            return JsonResponse(data)
        
        msg=""

        try:
            ormdata = self.model.objects.get(id=_id)
            ormdata.name=name
            ormdata.menuurl=menuurl
            ormdata.menutype=menutype
            ormdata.menuseq=menuseq
            ormdata.menupid=menupid

            ormdata.save()
            data={"code":1,"msg":msg}
        except IntegrityError as e:
            #得到异常消息
            msg=str(e.__cause__)
            #msg = "游戏名已经存在"
            logger.error(e.__cause__)
            data={"code":0,"msg":msg}

        return JsonResponse(data)

class MenuDelView(AdminUserRequiredMixin,TemplateView):
    """
    删除
    """
    model = Menu

    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        #得到单个要删除的id
        _id = request.POST.get("id")

        msg=""
        #删除
        self.model.objects.filter(id=_id).delete()
        data={"code":1,"msg":msg}

        return JsonResponse(data)