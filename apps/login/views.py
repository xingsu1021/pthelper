
from myauth.models import User
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from rest_framework.authtoken.models import Token

# Create your views here.
class LoginView(TemplateView):
    """
    登录
    """
    template_name = 'login/login.html'
    model = User

    def get(self, request, *args, **kwargs):
        """
        登录
        """
        #登录失效后，再次登录需要上次的url
        self.next = request.GET.get('next')

        if self.next == None:
            self.next = '/'

        return super(LoginView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'next': self.next
            # 'action': 'Asset list',
        }
        kwargs.update(context)
        return super(LoginView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        id = self.request.POST.get('id')
        username = request.POST.get("username")
        password = request.POST.get("password")
        #记住密码
        remember = request.POST.get("remember")

        if username == "" or username == None:
            data = {"code":0, "msg":"用户名不能为空"}
            return JsonResponse(data)

        if password == "" or password == None:
            data = {"code":0, "msg":"密码不能为空"}
            return JsonResponse(data)

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                # 更新token值
                try:
                    token = Token.objects.get(user=user)
                except:
                    #当用户token不存在，则创建token
                    token = Token.objects.create(user=user)
                #token.delete()
                #token = Token.objects.create(user=user)

                next = request.POST.get('next','/')

                data={"code": 1, "token":token.key, "url": next, "msg":"登录成功"}

            else:
                msg="账户禁止登录"
                data={"code": 0, "msg":msg}
        else:

            msg="用户名或密码错误"
            data={"code": 0, "msg":msg}

        return JsonResponse(data)

def logout(request):
    """
    登出
    """
    auth.logout(request)
    return HttpResponseRedirect('/login')