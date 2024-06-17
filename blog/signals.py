import re
import base64
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import strip_tags
from .models import Post
from social_api.tg_api import TGAPI
from social_api.vk_api import VKAPI

@receiver(post_save, sender=Post)
def send_social_notifications(sender, instance, created, **kwargs):
    if created and not instance.no_autopost:
        # Парсинг контента
        text = strip_tags(instance.content)
        images = re.findall(r'src="data:image/(.*?);base64,(.*?)"', instance.content)
        tags = instance.tags.all()
        tags_list = [tag.name for tag in tags]

        # Debug: Print extracted tags
        print(f"Extracted tags: {tags_list}")

        # Формирование тегов для Telegram и VK
        tags_str_telegram = ' '.join([f'#{tag}' for tag in tags_list])
        tags_str_vk = ' '.join([f'#{tag}@vrn_career' for tag in tags_list])

        # Debug: Print formatted tags
        print(f"Formatted tags for Telegram: {tags_str_telegram}")
        print(f"Formatted tags for VK: {tags_str_vk}")

        # Формирование подписи для изображения
        content_telegram = f'{text}\n\nTags: {tags_str_telegram}'
        content_vk = f'{text}\n\nTags: {tags_str_vk}'

        # Debug: Print final content
        print(f"Final content for Telegram: {content_telegram}")
        print(f"Final content for VK: {content_vk}")

        tg_api = TGAPI()
        vk_api = VKAPI()

        # Telegram
        media_group = []
        files = {}

        for index, (image_type, image_base64) in enumerate(images):
            # Декодирование изображения из base64
            image_data = base64.b64decode(image_base64)
            image_name = f'image_{index}.{image_type}'
            media = {
                'type': 'photo',
                'media': f'attach://{image_name}',
                'caption': content_telegram if index == 0 else '',
                'parse_mode': 'HTML'
            }
            media_group.append(media)
            files[image_name] = ('image/' + image_type, image_data)

        if media_group:
            response_media_group = tg_api.send_media_group(media_group, files)
        else:
            response_text = tg_api.send_post(instance.title, content_telegram)

        # Вывод ответа от сервера Telegram в консоль
        if media_group:
            print("Telegram Response (Media Group):", response_media_group)
        else:
            print("Telegram Response (Text):", response_text)

        # VK
        if images:
            vk_response = vk_api.send_post_with_images(instance.title, content_vk, images)
        else:
            vk_response = vk_api.send_post(instance.title, content_vk)

        print("VK Response:", vk_response)
