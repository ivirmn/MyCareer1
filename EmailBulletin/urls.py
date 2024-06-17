from django.contrib import admin
from django.urls import include, path

from EmailBulletin import views
from EmailBulletin.views import *

urlpatterns = [
path('create_bulletin/', create_bulletin, name='create_bulletin')
    ]