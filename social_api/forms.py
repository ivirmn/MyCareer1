from django import forms
from .models import VkApiAutopost, TgApiAutopost


class VkApiAutopostForm(forms.ModelForm):
    class Meta:
        model = VkApiAutopost
        fields = ['VkTokenAutopost', 'VkGroupId']


class TgApiAutopostForm(forms.ModelForm):
    class Meta:
        model = TgApiAutopost
        fields = ['TgTokenAutopost', 'TgChannelId']


class DebugVKPostForm(forms.Form):
    title = forms.CharField(max_length=200, label='Заголовок')
    content = forms.CharField(widget=forms.Textarea, label='Содержимое')


class DebugTGPostForm(forms.Form):
    title = forms.CharField(max_length=200, label='Заголовок')
    content = forms.CharField(widget=forms.Textarea, label='Содержимое')
