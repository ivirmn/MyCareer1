from django.contrib import admin
from . import models
admin.site.register(models.UserProfile)
admin.site.register(models.CareerCenter)
admin.site.register(models.Vacancy)
# admin.site.register(models.AdditionalImage)
admin.site.register(models.Messenger)
admin.site.register(models.Demand)
