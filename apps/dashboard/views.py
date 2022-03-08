from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from sites.models import SiteInfo

# Create your views here.
class DashboardListView(LoginRequiredMixin, TemplateView):
    """
    打开首页的控制台
    """
    template_name = 'dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        
        #配置站点总数
        sites_count = SiteInfo.objects.count()
        
        context = {
            'sites_num': sites_count,
            # 'action': 'Asset list',
        }
        kwargs.update(context)
        return super(DashboardListView, self).get_context_data(**kwargs)
