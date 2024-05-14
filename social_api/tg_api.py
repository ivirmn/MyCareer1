import requests
from social_api.models import TgApiAutopost

class TGAPI:
    def __init__(self):
        tg_token_instance = TgApiAutopost.objects.first()
        self.channel_id = '@ваш_телеграмм_канал'  # replace with your Telegram channel name
        self.bot_token = tg_token_instance.TgTokenAutopost  # replace with your Telegram bot token
        self.api_url = f'https://api.telegram.org/bot{self.bot_token}/'

    def send_post(self, title, content):
        params = {
            'chat_id': self.channel_id,
            'text': f'{title}\n\n{content}',
            'parse_mode': 'HTML',
            'disable_notification': True
        }
        response = requests.post(self.api_url + 'sendMessage', json=params)
        return response.json()
