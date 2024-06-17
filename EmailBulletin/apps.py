from django.apps import AppConfig


class EmailBulletinConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EmailBulletin'


class EmailBulletinConfig(AppConfig):
    name = 'EmailBulletin'

    def ready(self):
        import EmailBulletin.signals
