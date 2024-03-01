from django.apps import AppConfig

class XtraromsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xtraroms'
    
    def ready(self):
        import xtraroms.signals
