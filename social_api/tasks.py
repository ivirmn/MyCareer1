# from celery import shared_task
# from .vk_api import VKAPI
# from .tg_api import TelegramAPI
# from blog.models import Post
#
# @shared_task
# def autopost_to_social_networks(post):
#     Автопостинг в ВКонтакте
#    if post.autopost_to_vk:
#        vk_api = VKAPI()
#        vk_api.send_post(post.title, post.content)
#
#     Автопостинг в Телеграм
#    if post.autopost_to_tg:
#        tg_api = TelegramAPI()
#        tg_api.send_post(post.title, post.content)
