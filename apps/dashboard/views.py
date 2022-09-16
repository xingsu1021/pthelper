from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from sites.models import SiteInfo,SiteUser

# Create your views here.
class DashboardListView(LoginRequiredMixin, TemplateView):
    """
    打开首页的控制台
    """
    template_name = 'dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        
        #配置站点总数
        count_sites = SiteInfo.objects.count()
        
        html_data = []
        count_siteuser = SiteUser.objects.count()
        if count_siteuser == 0:
            html_data.append("<td><span class=\"layui-text\">请等待数据更新或手动点击更新</span></td>")
        else:
            ormdata_siteuser = SiteUser.objects.all()
            for i in ormdata_siteuser:
                d = "<tr><td><span class=\"layui-text\"><a>%s(%s)</a></span></td> \
                     <td>%s</td> \
                     <td>%s</td> \
                     <td>%s</td> \
                     <td align=\"center\">%s</td> \
                     <td>%s</td> \
                     <td>%s</td> \
                     <td>%s</td> \
                     <td>%s</td> \
                     <td>%s</td> \
                     </tr>" % (i.siteinfo_id.siteconfig_name,i.siteinfo_id.siteconfig_name_cn,
                               i.username,
                               i.uid,
                               i.level,
                               i.ratio,
                               i.seed_num,
                               i.totle_seed_size,
                               i.bonus,
                               i.score,
                               i.create_time
                               )
                html_data.append(d)
                
        context = {
            'sites_num': count_sites,
            'siteusers': "".join(html_data),
        }
        kwargs.update(context)
        return super(DashboardListView, self).get_context_data(**kwargs)
