import requests
import base64
from django.core.exceptions import ObjectDoesNotExist
from social_api.models import VkApiAutopost

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
            'message': content,  # Убираем дублирование заголовка
            'v': '5.199'
        }
        response = requests.get(self.api_url + 'wall.post', params=params)
        self.last_request_url = response.url
        print("VK Request URL:", self.last_request_url)  # Debug line
        print("VK Response:", response.json())  # Debug line
        return response.json()

    def send_post_with_images(self, title, content, images):
        attachments = []

        for image_type, image_base64 in images:
            image_data = base64.b64decode(image_base64)
            upload_url = self.get_upload_url()
            files = {'photo': ('photo.' + image_type, image_data, 'image/' + image_type)}
            response = requests.post(upload_url, files=files).json()

            if 'photo' in response:
                save_response = self.save_photo(response)
                if save_response.get('response'):
                    photo = save_response['response'][0]
                    attachments.append(f"photo{photo['owner_id']}_{photo['id']}")

        attachments_str = ','.join(attachments)
        params = {
            'access_token': self.access_token,
            'owner_id': self.owner_id,
            'from_group': 1,
            'message': content,  # Убираем дублирование заголовка
            'attachments': attachments_str,
            'v': '5.199'
        }
        response = requests.get(self.api_url + 'wall.post', params=params)
        self.last_request_url = response.url
        print("VK Request URL with images:", self.last_request_url)  # Debug line
        print("VK Response with images:", response.json())  # Debug line
        return response.json()

    def get_upload_url(self):
        params = {
            'access_token': self.access_token,
            'group_id': self.owner_id.lstrip('-'),
            'v': '5.199'
        }
        response = requests.get(self.api_url + 'photos.getWallUploadServer', params=params).json()
        return response['response']['upload_url']

    def save_photo(self, upload_response):
        params = {
            'access_token': self.access_token,
            'group_id': self.owner_id.lstrip('-'),
            'photo': upload_response['photo'],
            'server': upload_response['server'],
            'hash': upload_response['hash'],
            'v': '5.199'
        }
        response = requests.get(self.api_url + 'photos.saveWallPhoto', params=params)
        return response.json()

    def check_token(self):
        params = {
            'access_token': self.access_token,
            'v': '5.199'
        }
        response = requests.get(self.api_url + 'groups.getById', params=params)
        if response.json().get('response'):
            group = response.json()['response'][0]
            return True, group['name'], self.get_user_info()
        return False, None, None

    def get_user_info(self):
        params = {
            'access_token': self.access_token,
            'v': '5.199'
        }
        response = requests.get(self.api_url + 'account.getInfo', params=params)
        if response.json().get('response'):
            user = response.json()['response']['user']
            return user['first_name'], user['last_name']
        return None, None
