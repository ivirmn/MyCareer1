from django.http import Http404
# ваше_приложение/views.py

from django.shortcuts import render, get_object_or_404
from survey.models import Response  # Обратите внимание, что используется Response (не response)


def survey_response_detail(request, survey_id, user_id):
    # Получаем объект респонза из внешней библиотеки
    responses = Response.objects.filter(survey_id=survey_id, user_id=user_id)
    response_obj = responses.first()

    return render(request, 'survey-id.html', {'response': response_obj})

def survey_debug(request):
    return render(request, )
# Create your views here.
