import time
from collections import deque


import vk
from django.core.exceptions import ObjectDoesNotExist
from social_api.models import VkApiAutopost  # Импортируйте модель VkApiAutopost
import requests

#session = vk.Session(access_token='self.access_token')
#api = vk.API(session)
class VKAPI:
    def __init__(self):
        try:
            vk_token_instance = VkApiAutopost.objects.first()
            self.access_token = vk_token_instance.VkTokenAutopost
            self.api_url = 'https://api.vk.com/method/'
            self.owner_id = f'-{vk_token_instance.VkGroupId}'
            self.last_request_url = None
        except ObjectDoesNotExist:
            raise Exception('VK API token and group ID not found in the database')

    def send_post(self, title, content):
        params = {
            'access_token': self.access_token,
            'owner_id': self.owner_id,
            'from_group': 1,
            'message': f'{title}\n\n{content}',
            'v': '5.199'
        }
        self.last_request_url = requests.get(self.api_url + 'wall.post', params=params).url
        response = requests.get(self.api_url + 'wall.post', params=params)
        return response.json()

    class TelegramAPI:
        def __init__(self, bot_token):
            self.bot_token = bot_token
            self.api_url = f'https://api.telegram.org/bot{self.bot_token}/'

        def check_auth(self):
            response = requests.get(self.api_url + 'getMe')

            # Сохраните URL запроса в контексте
            self.last_request_url = response.url

            if response.status_code == 200:
                return response.json()
            else:
                return None