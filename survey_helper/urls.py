from survey import models
from survey.models import *
from .views import *
from django.urls import include, path
urlpatterns = [
path('', include('blog.urls')),
path('survey_responses/<int:survey_id>/<int:user_id>/', survey_response_detail, name='survey_response_detail'),
path('/surveydebug.html', survey_debug, name='survey_debug')
#path('')
]