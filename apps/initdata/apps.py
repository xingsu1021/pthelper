from django.apps import AppConfig
from django.db.models.signals import post_migrate

def do_init_data(sender, **kwargs):
    from initdata.initDatas import init_datas
    init_datas()
    
class InitdataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'initdata'

    def ready(self):
        post_migrate.connect(do_init_data, sender=self)