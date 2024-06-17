from ckeditor.widgets import CKEditorWidget
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import *
from .forms import FreeFormNewsletterForm
from .models import UserProfile
from social_api.tg_api import TGAPI
from EmailBulletin import forms
from EmailBulletin.models import EmailTemplate


# Create your views here.


@login_required
def create_bulletin(request):
    if request.method == 'POST':
        form = FreeFormNewsletterForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            template = form.cleaned_data['template']

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
                tg_api.send_bulletin(subject, body, user)

    else:
        form = FreeFormNewsletterForm()

    return render(request, 'create_bulletin.html', {'form': form})