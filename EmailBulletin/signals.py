from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EmailTemplate
from social_api.tg_api import TGAPI
from .models import UserProfile

@receiver(post_save, sender=EmailTemplate)
def send_bulletin_signal(sender, instance, created, **kwargs):
    if created:
        # Получаем пользователей, которые не суперпользователи, согласны на рассылку и активны
        users = UserProfile.objects.filter(
            is_superuser=False,
            agreed_for_email_bulletins=True,
            is_active=True,
            have_telegram=True
        )

        tg_api = TGAPI()

        for user in users:
            print(f"Sending bulletin to user: {user.email}, Telegram ID: {user.telegram_id}")  # Debug line
            tg_api.send_bulletin(instance.subject, instance.body, user)
