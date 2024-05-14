from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User

from MyCareer.models import UserProfile


# Create your models here.

class EmailTemplate(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = RichTextField()


#
class EmailCampaign(models.Model):
    name = models.CharField(max_length=255)
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE)
    send_date = models.DateTimeField()
    users = models.ManyToManyField(UserProfile)
