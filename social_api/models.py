from django.db import models


# Create your models here.
class VkApiAutopost(models.Model):
    VkTokenAutopost = models.CharField(max_length=1000, blank=True)
    VkGroupId = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.VkTokenAutopost


class TgApiAutopost(models.Model):
    TgTokenAutopost = models.CharField(max_length=1000, blank=True)
    TgChannelId = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.TgTokenAutopost
