from ckeditor.widgets import CKEditorWidget
from .models import EmailTemplate, EmailCampaign
from django import forms
#
# class EmailTemplateForm(forms.ModelForm):
#     body = forms.CharField(widget=CKEditorWidget())
#
#     class Meta:
#         model = EmailTemplate
#         fields = ('name', 'subject', 'body')
#
# class EmailCampaignForm(forms.ModelForm):
#     class Meta:
#         model = EmailCampaign
#         fields = ('name', 'template', 'users')
class FreeFormNewsletterForm(forms.Form):
    subject = forms.CharField(max_length=255)
    body = forms.CharField(widget=CKEditorWidget())
    template = forms.ModelChoiceField(queryset=EmailTemplate.objects.all())
