from django.apps import AppConfig


class ManagementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "management"
    verbose_name = 'Компьютерлік техниканы жөндеу'

default_app_config = 'management.YourAppConfig'
