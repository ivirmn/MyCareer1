from django.contrib import admin
from django.urls import include, path

from social_api import views
from social_api.views import *

urlpatterns = [
    path('socialauthview', views.SocialAuthView, name='social_auth_view'),
    path('autopost_tokens/', autopost_tokens_view, name='autopost_tokens'),
    path('debug_vk_post/', debug_vk_post_view, name='debug_vk_post'),
    path('debug_tg_post/', debug_tg_post_view, name='debug_vk_post')
]
