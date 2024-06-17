from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import VkApiAutopostForm, TgApiAutopostForm, DebugVKPostForm, DebugTGPostForm
from .models import *
from .vk_api import VKAPI
from .tg_api import TGAPI


# from .tg_api import TGAPI
# Create your views here.
# class SocialAuthView(TemplateView):
#     template_name = 'social_auth.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         vk_token = self.request.GET.get('vk_token')
#         tg_token = self.request.GET.get('tg_token')
#
#         if vk_token:
#             vk_api = VKAPI(token=vk_token)
#             vk_user = vk_api.get_user_info()
#             context['vk_user'] = vk_user
#
#         if tg_token:
#             tg_api = TGAPI(token=tg_token)
#             tg_user = tg_api.get_user_info()
#             context['tg_user'] = tg_user
#
#         return context
@user_passes_test(lambda u: u.is_superuser)
def SocialAuthView(request):
    return render(request, 'social_auth.html')


@user_passes_test(lambda u: u.is_superuser)
def autopost_tokens_view(request):
    if request.method == 'POST':
        vk_form = VkApiAutopostForm(request.POST)
        tg_form = TgApiAutopostForm(request.POST)

        if vk_form.is_valid() and tg_form.is_valid():
            vk_token_instance = VkApiAutopost.objects.first()
            tg_token_instance = TgApiAutopost.objects.first()

            if vk_token_instance:
                vk_token_instance.VkTokenAutopost = vk_form.cleaned_data['VkTokenAutopost']
                vk_token_instance.VkGroupId = vk_form.cleaned_data['VkGroupId']
                vk_token_instance.save()
            else:
                vk_form.save()

            if tg_token_instance:
                tg_token_instance.TgTokenAutopost = tg_form.cleaned_data['TgTokenAutopost']
                tg_token_instance.TgChannelId = tg_form.cleaned_data['TgChannelId']
                tg_token_instance.save()
            else:
                tg_form.save()

            return redirect('success_url')  # Укажите URL для перенаправления после успешного сохранения

    else:
        vk_form = VkApiAutopostForm()
        tg_form = TgApiAutopostForm()

        vk_token_instance = VkApiAutopost.objects.first()
        tg_token_instance = TgApiAutopost.objects.first()

    context = {
        'vk_form': vk_form,
        'tg_form': tg_form,
        'vk_token_instance': vk_token_instance,
        'tg_token_instance': tg_token_instance,
    }

    vk_info = None
    tg_info = None

    if vk_token_instance:
        vk_api = VKAPI()
        vk_token_valid, group_name, user_info = vk_api.check_token()
        vk_info = {'valid': vk_token_valid, 'group_name': group_name, 'user_info': user_info}

    if tg_token_instance:
        tg_api = TGAPI()
        tg_token_valid, first_name, username = tg_api.check_token()
        tg_info = {'valid': tg_token_valid, 'first_name': first_name, 'username': username}

    context.update({
        'vk_info': vk_info,
        'tg_info': tg_info,
    })

    return render(request, 'autopost_tokens.html', context)



@user_passes_test(lambda u: u.is_superuser)
class DebugVKAPIView:
    def __init__(self):
        self.vk_api = VKAPI()

    def get_vk_token_and_group(self):
        try:
            vk_token_instance = VkApiAutopost.objects.first()
            return vk_token_instance.VkTokenAutopost, vk_token_instance.VkGroupId
        except VkApiAutopost.DoesNotExist:
            return None, None


@user_passes_test(lambda u: u.is_superuser)
def debug_vk_post_view(request):
    debug_vk_api = DebugVKAPIView()

    if request.method == 'POST':
        form = DebugVKPostForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            response = debug_vk_api.vk_api.send_post(title, content)

            # Обновите ответ сервера VK в контексте
            context = {
                'form': form,
                'vk_response': response,
            }

            # Добавьте информацию о токене, ID группы и других данных в контекст
            vk_token, vk_group_id = debug_vk_api.get_vk_token_and_group()

            vk_auth_info = None
            if vk_token:
                vk_auth_info = debug_vk_api.vk_api.check_auth()

                # Извлеките необходимые данные из vk_auth_info
                vk_user_id = vk_auth_info.get('response', [])[0].get('uid')
                vk_user_name = vk_auth_info.get('response', [])[0].get('first_name')
                vk_user_lastname = vk_auth_info.get('response', [])[0].get('last_name')

            context.update({
                'vk_token': vk_token,
                'vk_group_id': vk_group_id,
                'vk_auth_info': vk_auth_info,
                'vk_user_id': vk_user_id,
                'vk_user_name': vk_user_name,
                'vk_user_lastname': vk_user_lastname,
                'vk_request_url': debug_vk_api.vk_api.last_request_url,
            })

            # Перенаправление после успешной отправки формы
            return render(request, 'debug_vk_post.html', context)

    else:
        form = DebugVKPostForm()

    vk_token, vk_group_id = debug_vk_api.get_vk_token_and_group()

    vk_auth_info = None
    if vk_token:
        vk_auth_info = debug_vk_api.vk_api.check_auth()

        # Извлеките необходимые данные из vk_auth_info
        vk_user_id = vk_auth_info.get('response', [])[0].get('uid')
        vk_user_name = vk_auth_info.get('response', [])[0].get('first_name')
        vk_user_lastname = vk_auth_info.get('response', [])[0].get('last_name')

    context = {
        'form': form,
        'vk_token': vk_token,
        'vk_group_id': vk_group_id,
        'vk_auth_info': vk_auth_info,
        'vk_user_id': vk_user_id,
        'vk_user_name': vk_user_name,
        'vk_user_lastname': vk_user_lastname,
        'vk_request_url': debug_vk_api.vk_api.last_request_url,
        'vk_response': None,  # Добавьте ответ сервера VK в контекст
    }
    return render(request, 'debug_vk_post.html', context)


class DebugTGAPIView:
    def __init__(self):
        self.telegram_api = TGAPI()

    def get_tg_token(self):
        try:
            tg_token_instance = TgApiAutopost.objects.first()
            return tg_token_instance.TgTokenAutopost
        except TgApiAutopost.DoesNotExist:
            return None


@user_passes_test(lambda u: u.is_superuser)
def debug_tg_post_view(request):
    debug_tg_api = DebugTGAPIView()

    if request.method == 'POST':
        form = DebugTGPostForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            response = debug_tg_api.telegram_api.send_post(title, content)

            # Обновите ответ сервера Telegram в контексте
            context = {
                'form': DebugTGPostForm(),  # Отобразите пустую форму после отправки
                'tg_response': response,
            }

            # Добавьте информацию о токене, ID канала и других данных в контекст
            tg_token = debug_tg_api.get_tg_token()

            tg_auth_info = None
            if tg_token:
                tg_auth_info = debug_tg_api.telegram_api.check_auth()

                # Извлеките необходимые данные из tg_auth_info
                tg_user_id = tg_auth_info.get('id')
                tg_user_name = tg_auth_info.get('first_name')
                tg_user_lastname = tg_auth_info.get('last_name')

            # Инициализируйте переменные, если tg_auth_info равно None
            if tg_auth_info is None:
                tg_user_id = None
                tg_user_name = None
                tg_user_lastname = None

            context.update({
                'tg_token': tg_token,
                'tg_auth_info': tg_auth_info,
                'tg_user_id': tg_user_id,
                'tg_user_name': tg_user_name,
                'tg_user_lastname': tg_user_lastname,
                'tg_request_url': debug_tg_api.telegram_api.last_request_url,
            })

            # Перенаправление после успешной отправки формы
            return render(request, 'debug_tg_post.html', context)

    else:
        form = DebugTGPostForm()

    tg_token = debug_tg_api.get_tg_token()

    tg_auth_info = None
    if tg_token:
        tg_auth_info = debug_tg_api.telegram_api.check_auth()

        # Извлеките необходимые данные из tg_auth_info
        tg_user_id = tg_auth_info.get('id')
        tg_user_name = tg_auth_info.get('first_name')
        tg_user_lastname = tg_auth_info.get('last_name')

    # Инициализируйте переменные, если tg_auth_info равно None
    if tg_auth_info is None:
        tg_user_id = None
        tg_user_name = None
        tg_user_lastname = None

    context = {
        'form': form,  # Добавьте форму в контекст
        'tg_token': tg_token,
        'tg_auth_info': tg_auth_info,
        'tg_user_id': tg_user_id,
        'tg_user_name': tg_user_name,
        'tg_user_lastname': tg_user_lastname,
        'tg_request_url': debug_tg_api.telegram_api.last_request_url,
        'tg_response': None,  # Добавьте ответ сервера Telegram в контекст
    }
    vk_info = None
    tg_info = None


    return render(request, 'debug_tg_post.html', context)
