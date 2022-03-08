
from django.conf import settings

"""
模板直接使用settings变量
"""


def get_global_settings(request):
    context = {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_URL': settings.SITE_URL,
        'SITE_VERSION': settings.SITE_VERSION,
        'SITE_COPYRIGHT': settings.SITE_COPYRIGHT,
        'SITE_NAME_COPYRIGHT': settings.SITE_NAME_COPYRIGHT,
    }
    return context
