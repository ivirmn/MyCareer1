from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from MyCareer.models import Vacancy, Messenger
from MyCareer.serializers import VacancySerializer
from MyCareer.forms import UserProfileForm, VacancyForm, EmployerRegistrationForm, ApplicantRegistrationForm, \
    UserProfileEditForm, DemandForm
from MyCareer.forms import UserProfile
from MyCareer.models import Message, Demand, Counter
from django.views import View
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
import csv
from django.http import HttpResponse
from openpyxl import Workbook


def vacancy_list(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'vacancy_test.html', {'vacancies': vacancies})


def test_template(request):
    return render(request, 'testtemplate.html')


def index(request):
    return render(request, 'index.html')


def vacancy_detail(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    return render(request, 'vacancy_detail.html', {'vacancy': vacancy})


def create_user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Additional logic if needed
            return redirect('profile.html')
    else:
        form = UserProfileForm()
    return render(request, 'regtest.html', {'form': form})


def see_user_profile(request):
    user = request.user  # Получить текущего пользователя
    return render(request, 'profile.html', {'user': user})


def messenger_test(request):
    messengers = Messenger.objects.all()
    return render(request, 'test_messenger.html', {'messengers': messengers})


def send_message(request):
    if request.method == 'POST':
        messenger_id = request.POST.get('messenger_id')
        person_id = request.POST.get('person_id')
        message_text = request.POST.get('message')

        # Retrieve the messenger based on the provided ID
        try:
            messenger = Messenger.objects.get(id=messenger_id)
        except Messenger.DoesNotExist:
            return redirect('messenger_test')  # Redirect to messenger test if messenger does not exist

        # Perform any necessary validations and message sending logic here
        # ...

        # Create a new message
        message = Message.objects.create(messenger=messenger, person_id=person_id, message=message_text)

        # Once the message is sent, you can redirect to a success page or back to the messenger view
        return redirect('messenger_test')  # Redirect to the messenger test page

    return redirect('messenger_test')  # Redirect to the messenger test page if not a POST request


def messenger_test(request):
    messengers = Messenger.objects.all()
    print(messengers)  # Check the output in the console
    return render(request, 'test_messenger.html', {'messengers': messengers})


def job_search(request):
    keyword = request.GET.get('keyword')

    if keyword:
        vacancies = Vacancy.objects.filter(title__icontains=keyword)
    else:
        vacancies = []

    return render(request, 'test-search.html', {'vacancies': vacancies})


def registration_plug(request):
    return render(request, 'registration-plug.html')


def create_vacancy(request):
    if request.method == 'POST':
        form = VacancyForm(request.POST, request.FILES)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.employer = request.user.user
            vacancy.save()
            return redirect('vacancy_detail', vacancy_id=vacancy.id)
    else:
        form = VacancyForm()

    return render(request, 'create_vacancy.html', {'form': form})


class VacancyCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)

        def send_message(request):
            if request.method == 'POST':
                sender_id = request.POST.get('sender_id')
                recipient_id = request.POST.get('recipient_id')
                message_text = request.POST.get('message')
                try:
                    sender = UserProfile.objects.get(id=sender_id)
                    recipient = UserProfile.objects.get(id=recipient_id)
                except UserProfile.DoesNotExist:
                    return redirect('messenger_test')  # Redirect if sender or recipient does not exist
                message = Message.objects.create(sender=sender, recipient=recipient, message=message_text)
                return redirect('messenger_test')
            return redirect('messenger_test')


def employer_registration(request):
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect('profile.html')
    else:
        form = EmployerRegistrationForm()
    return render(request, 'employer-registration.html', {'form': form})


def applicant_registration(request):
    if request.method == 'POST':
        form = ApplicantRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Additional logic if needed
            return redirect('profile.html')
    else:
        form = ApplicantRegistrationForm()
    return render(request, 'applicant-registration.html', {'form': form})


def edit_user_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile.html')
    else:
        form = UserProfileEditForm(instance=user)
    return render(request, 'editprofile.html', {'form': form})


class AddDemandView(View):
    def get(self, request):
        return render(request, 'add_demand.html')

    @method_decorator(csrf_protect)
    def post(self, request):
        reason = request.POST.get('reason')
        salary = request.POST.get('salary')
        have_whatsapp = request.POST.get('have_whatsapp') == 'on'
        have_viber = request.POST.get('have_viber') == 'on'
        have_telegram = request.POST.get('have_telegram') == 'on'
        faculty = request.POST.get('faculty')
        target = request.POST.get('target')
        stage = request.POST.get('stage')
        result = request.POST.get('result')

        demand = Demand(
            reason=reason,
            salary=salary,
            have_whatsapp=have_whatsapp,
            have_viber=have_viber,
            have_telegram=have_telegram,
            faculty=faculty,
            target=target,
            stage=stage,
            result=result
        )
        demand.save()

        return render(request, 'add_demand.html')


def demand_interface(request):
    demands = Demand.objects.all()
    counter = Counter.objects.first()
    form = DemandForm()

    if request.method == 'POST':
        form = DemandForm(request.POST)
        if form.is_valid():
            form.save()

    context = {
        'form': form,
        'demands': demands,
        'counter': counter,
    }
    return render(request, 'demand-interface.html', context)

def update_demand(request, demand_id):
    demand = Demand.objects.get(id=demand_id)
    if request.method == 'POST':
        stage = request.POST.get('stage')
        result = request.POST.get('result')

        demand.stage = stage
        demand.result = result
        demand.save()

    return redirect('demand_interface')

def delete_demand(request, demand_id):
    demand = Demand.objects.get(id=demand_id)
    demand.delete()

    return redirect('demand_interface')


class ExportDemandsCSVView(View):
    def get(self, request):
        # Получаем все заявки
        demands = Demand.objects.all()

        # Создаем объект HttpResponse с типом контента "text/csv"
        response: HttpResponse = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="demands.csv"'

        # Создаем объект writer для записи данных в CSV
        writer = csv.writer(response)

        # Записываем заголовки столбцов
        writer.writerow(['Reason', 'Salary', 'Faculty', 'Target', 'Stage', 'Result'])

        # Записываем данные заявок
        for demand in demands:
            writer.writerow([demand.reason, demand.salary, demand.faculty, demand.target, demand.stage, demand.result])

        return response

class ExportDemandsExcelView(View):
    def get(self, request):
        # Получаем все заявки
        demands = Demand.objects.all()

        # Создаем объект Workbook
        workbook = Workbook()

        # Получаем активный лист
        sheet = workbook.active

        # Записываем заголовки столбцов
        sheet.append(['Reason', 'Salary', 'Faculty', 'Target', 'Stage', 'Result'])

        # Записываем данные заявок
        for demand in demands:
            sheet.append([demand.reason, demand.salary, demand.faculty, demand.target, demand.stage, demand.result])

        # Создаем HttpResponse с типом контента "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="demands.xlsx"'

        # Сохраняем Workbook в HttpResponse
        workbook.save(response)

        return response

def error_403(request, exception):
    return render(request, '403.html', status=403)

def error_500(request):
    return render(request, '500.html', status=500)

def error_502(request):
    return render(request, '502.html', status=502)