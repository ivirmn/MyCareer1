import requests
import base64
from social_api.models import TgApiAutopost

class TGAPI:
    def __init__(self):
        tg_token_instance = TgApiAutopost.objects.first()
        self.channel_id = tg_token_instance.TgChannelId
        self.bot_token = tg_token_instance.TgTokenAutopost
        self.api_url = f'https://api.telegram.org/bot{self.bot_token}/'
        self.last_request_url = None
        print(f"TGAPI initialized with channel_id: {self.channel_id} and bot_token: {self.bot_token[:10]}...")  # Debug line

    def send_post(self, title, content):
        params = {
            'chat_id': self.channel_id,
            'text': content,
            'parse_mode': 'HTML',
            'disable_notification': True
        }
        response = requests.post(self.api_url + 'sendMessage', params=params)
        self.last_request_url = response.url
        print("Telegram Request URL:", self.last_request_url)  # Debug line
        print("Telegram Response:", response.json())  # Debug line
        return response.json()

    def send_bulletin(self, subject, content, user):
        message = f"<b>{subject}</b>\n\n{content}"
        params = {
            'chat_id': user.telegram_id,
            'text': message,
            'parse_mode': 'HTML',
            'disable_notification': True
        }
        response = requests.post(self.api_url + 'sendMessage', params=params)
        self.last_request_url = response.url
        print(f"Sending bulletin to user: {user.email}, Telegram ID: {user.telegram_id}")  # Debug line
        print(f"Bulletin Subject: {subject}")  # Debug line
        print(f"Bulletin Content: {content}")  # Debug line
        print("Telegram Bulletin Request URL:", self.last_request_url)  # Debug line
        print("Telegram Bulletin Response URL:", response.url)  # Debug line
        print("Telegram Bulletin Response:", response.json())  # Debug line
        return response.json()

    def send_media_group(self, media_group, files):
        data = {
            'chat_id': self.channel_id,
            'media': media_group,
            'disable_notification': True
        }
        response = requests.post(self.api_url + 'sendMediaGroup', data=data, files=files)
        self.last_request_url = response.url
        print("Telegram Request URL (Media Group):", self.last_request_url)  # Debug line
        print("Telegram Response (Media Group):", response.json())  # Debug line
        return response.json()

    def check_token(self):
        response = requests.get(self.api_url + 'getMe')
        if response.json().get('ok'):
            return True, response.json()['result']['first_name'], response.json()['result']['username']
        return False, None, None


# import requests
# import base64
# from social_api.models import TgApiAutopost
#
# class TGAPI:
#     def __init__(self):
#         tg_token_instance = TgApiAutopost.objects.first()
#         self.channel_id = tg_token_instance.TgChannelId
#         self.bot_token = tg_token_instance.TgTokenAutopost  # replace with your Telegram bot token
#         self.api_url = f'https://api.telegram.org/bot{self.bot_token}/'
#         self.last_request_url = None
#
#     def send_post(self, title, content):
#         params = {
#             'chat_id': self.channel_id,
#             'text': content,
#             'parse_mode': 'HTML',
#             'disable_notification': True
#         }
#         response = requests.post(self.api_url + 'sendMessage', params=params)
#         self.last_request_url = response.url
#         print("Telegram Request URL:", self.last_request_url)  # Debug line
#         print("Telegram Response:", response.json())  # Debug line
#         return response.json()
#
#     def send_media_group(self, media_group, files):
#         data = {
#             'chat_id': self.channel_id,
#             'media': media_group,
#             'disable_notification': True
#         }
#         response = requests.post(self.api_url + 'sendMediaGroup', data=data, files=files)
#         self.last_request_url = response.url
#         print("Telegram Request URL (Media Group):", self.last_request_url)  # Debug line
#         print("Telegram Response (Media Group):", response.json())  # Debug line
#         return response.json()
#
#     def check_token(self):
#         response = requests.get(self.api_url + 'getMe')
#         if response.json().get('ok'):
#             return True, response.json()['result']['first_name'], response.json()['result']['username']
#         return False, None, None
