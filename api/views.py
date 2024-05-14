from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
# from MyCareer.models import Vacancy, Messenger
# from MyCareer.serializers import VacancySerializer
from MyCareer.forms import UserProfileEditForm, DemandForm, RegistrationForm
from MyCareer.forms import UserProfile, SurveyForm, QuestionForm, EditQuestionForm
from MyCareer.models import Demand, Counter, Survey, Question, Answer
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.permissions import IsAuthenticated
import csv
from django.http import HttpResponse, JsonResponse
from openpyxl import Workbook
from datetime import datetime

from api.serializers import UserProfileSerializer


# def vacancy_list(request):
#     vacancies = Vacancy.objects.all()
#     return render(request, 'vacancy_test.html', {'vacancies': vacancies})
#
#
# def test_template(request):
#     return render(request, 'testtemplate.html')


def index(request):
    return render(request, 'index.html')


# def vacancy_detail(request, vacancy_id):
#     vacancy = get_object_or_404(Vacancy, id=vacancy_id)
#     return render(request, 'vacancy_detail.html', {'vacancy': vacancy})


# def create_user_profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save()
#             # Additional logic if needed
#             return redirect('profile.html')
#     else:
#         form = UserProfileForm()
#     return render(request, 'regtest.html', {'form': form})


@login_required(login_url='login')  # 'login' - это URL-шаблон для страницы входа
def see_user_profile(request):
    user = request.user  # Получить текущего пользователя
    return render(request, 'profile.html', {'user': user})


# def messenger_test(request):
#     messengers = Messenger.objects.all()
#     return render(request, 'test_messenger.html', {'messengers': messengers})
#
#
# def send_message(request):
#     if request.method == 'POST':
#         messenger_id = request.POST.get('messenger_id')
#         person_id = request.POST.get('person_id')
#         message_text = request.POST.get('message')
#
#         # Retrieve the messenger based on the provided ID
#         try:
#             messenger = Messenger.objects.get(id=messenger_id)
#         except Messenger.DoesNotExist:
#             return redirect('messenger_test')  # Redirect to messenger test if messenger does not exist
#
#         # Perform any necessary validations and message sending logic here
#         # ...
#
#         # Create a new message
#         message = Message.objects.create(messenger=messenger, person_id=person_id, message=message_text)
#
#         # Once the message is sent, you can redirect to a success page or back to the messenger view
#         return redirect('messenger_test')  # Redirect to the messenger test page
#
#     return redirect('messenger_test')  # Redirect to the messenger test page if not a POST request


# def messenger_test(request):
#     messengers = Messenger.objects.all()
#     print(messengers)  # Check the output in the console
#     return render(request, 'test_messenger.html', {'messengers': messengers})


# def job_search(request):
#     keyword = request.GET.get('keyword')
#
#     if keyword:
#         vacancies = Vacancy.objects.filter(title__icontains=keyword)
#     else:
#         vacancies = []
#
#     return render(request, 'test-search.html', {'vacancies': vacancies})


# def registration_plug(request):
#     return render(request, 'registration-plug.html')


# def create_vacancy(request):
#     if request.method == 'POST':
#         form = VacancyForm(request.POST, request.FILES)
#         if form.is_valid():
#             vacancy = form.save(commit=False)
#             vacancy.employer = request.user.user
#             vacancy.save()
#             return redirect('vacancy_detail', vacancy_id=vacancy.id)
#     else:
#         form = VacancyForm()
#
#     return render(request, 'create_vacancy.html', {'form': form})


# class VacancyCreateView(generics.CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Vacancy.objects.all()
#     serializer_class = VacancySerializer
#
#     def perform_create(self, serializer):
#         serializer.save(employer=self.request.user)
#
#         def send_message(request):
#             if request.method == 'POST':
#                 sender_id = request.POST.get('sender_id')
#                 recipient_id = request.POST.get('recipient_id')
#                 message_text = request.POST.get('message')
#                 try:
#                     sender = UserProfile.objects.get(id=sender_id)
#                     recipient = UserProfile.objects.get(id=recipient_id)
#                 except UserProfile.DoesNotExist:
#                     return redirect('messenger_test')  # Redirect if sender or recipient does not exist
#                 message = Message.objects.create(sender=sender, recipient=recipient, message=message_text)
#                 return redirect('messenger_test')
#             return redirect('messenger_test')


# def employer_registration(request):
#     if request.method == 'POST':
#         form = EmployerRegistrationForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save()
#             return redirect('profile.html')
#     else:
#         form = EmployerRegistrationForm()
#     return render(request, 'employer-registration.html', {'form': form})


# def applicant_registration(request):
#     if request.method == 'POST':
#         form = ApplicantRegistrationForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save()
#             # Additional logic if needed
#             return redirect('profile.html')
#     else:
#         form = ApplicantRegistrationForm()
#     return render(request, 'applicant-registration.html', {'form': form})


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


''' class AddDemandView(View):
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
        phonenumber = request.POST.get('phonenumber')

        demand = Demand(
            reason=reason,
            salary=salary,
            have_whatsapp=have_whatsapp,
            have_viber=have_viber,
            have_telegram=have_telegram,
            faculty=faculty,
            target=target,
            stage=stage,
            result=result,
            phonenumber=phonenumber,
        )
        demand.save()

        return render(request, 'add_demand.html')
'''


@login_required
def create_demand(request):
    user_profile = UserProfile.objects.get(email=request.user.email)

    if request.method == 'POST':
        target = request.POST.get('target')

        # Создание новой заявки
        demand = Demand.objects.create(
            user_profile=user_profile,
            target=target
        )

        # Редирект на страницу профиля
        return redirect('profile')

    return render(request, 'create-demand.html', {'user_profile': user_profile})


@user_passes_test(lambda u: u.is_superuser)
def demand_interface(request):
    demands = Demand.objects.all()
    counter = Counter.objects.first()
    form = DemandForm()

    if request.method == 'POST':
        form = DemandForm(request.POST)
        if form.is_valid():
            form.save()

    show_archived = request.GET.get('show_archived')  # Получение значения параметра show_archived из URL

    # Фильтрация заявок на основе параметра show_archived
    if show_archived:
        archived_demands = Demand.objects.filter(isArchived=True)
    else:
        archived_demands = None

    context = {
        'form': form,
        'demands': demands,
        'counter': counter,
        'archived_demands': archived_demands,
        'show_archived': show_archived,
    }
    return render(request, 'demand-interface.html', context)


# def update_demand(request, demand_id):
#     demand = Demand.objects.get(id=demand_id)
#     if request.method == 'POST':
#         stage = request.POST.get('stage')
#         result = request.POST.get('result')
#
#         demand.stage = stage
#         demand.result = result
#         demand.save()
#
#     return redirect('demand_interface')

def update_demand(request, demand_id):
    if request.method == "POST":
        new_stage = request.POST.get('stage')
        new_result = request.POST.get('result')
        new_comment = request.POST.get('comment')

        try:
            demand = Demand.objects.get(pk=demand_id)
            demand.stage = new_stage
            demand.result = new_result
            demand.comment = new_comment
            demand.save()
            return JsonResponse({'success': True})
        except Demand.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Заявка не найдена'})

    return JsonResponse({'success': False, 'error': 'Неверный метод запроса'})

def delete_demand(request, demand_id):
    demand = Demand.objects.get(id=demand_id)
    demand.delete()

    return redirect('demand_interface')


def archive_demand(request, demand_id):
    demand = get_object_or_404(Demand, pk=demand_id)
    demand.isArchived = True
    demand.save()
    return redirect('demand_interface')


@user_passes_test(lambda u: u.is_superuser)
def export_demands_csv(request):
    # Получаем все заявки
    demands = Demand.objects.all()

    # Создаем текущую дату и время
    now = datetime.now()
    timestamp = now.strftime("%Y_%m_%d_%H:%M:%S")

    # Создаем объект HttpResponse с типом контента "text/csv"
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="demands_{timestamp}.csv"'

    # Создаем объект writer для записи данных в CSV
    writer = csv.writer(response)

    # Записываем заголовки столбцов
    writer.writerow(['Date', 'Email', 'First name', 'Surname', 'Patronymic', 'Phonenumber', 'Faculty',
                     'Course', 'Target', 'Stage', 'Result', 'Comment'])

    # Записываем данные заявок
    for demand in demands:
        user_profile = demand.user_profile
        writer.writerow([
            demand.date_created,
            user_profile.email if user_profile else "",  # Проверка на наличие user_profile
            user_profile.firstname if user_profile else "",
            user_profile.surname if user_profile else "",
            user_profile.patronymic if user_profile else "",
            user_profile.phonenumber if user_profile else "",
            user_profile.faculty if user_profile else "",
            user_profile.course if user_profile else "",
            demand.target,
            demand.stage,
            demand.result,
            demand.comment
        ])

    return response
@user_passes_test(lambda u: u.is_superuser)
def export_active_demands_csv(request):
    def get(self, request):
        # Получаем все заявки
        demands = Demand.objects.all()

        # Создаем текущую дату и время
        now = datetime.now()
        timestamp = now.strftime("%Y_%m_%d_%H:%M:%S")

        # Создаем объект HttpResponse с типом контента "text/csv"
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="active_demands_{timestamp}.csv"'

        # Создаем объект writer для записи данных в CSV
        writer = csv.writer(response)

        # Записываем заголовки столбцов
        writer.writerow(['Date', 'Email', 'First name', 'Surname', 'Patronymic', 'Phonenumber', 'Faculty',
                         'Course', 'Target', 'Stage', 'Result', 'Comment'])

        # Записываем данные заявок
        for demand in demands:
            user_profile = demand.user_profile
            writer.writerow([
                demand.date_created,
                user_profile.email if user_profile else "",  # Проверка на наличие user_profile
                user_profile.firstname if user_profile else "",
                user_profile.surname if user_profile else "",
                user_profile.patronymic if user_profile else "",
                user_profile.phonenumber if user_profile else "",
                user_profile.faculty if user_profile else "",
                user_profile.course if user_profile else "",
                demand.target,
                demand.stage,
                demand.result,
                demand.comment
            ])

        return response

@user_passes_test(lambda u: u.is_superuser)
def article_editor(request):
    return render(request, 'article-editor.html')
    return render(request, 'article-editor.html')
@user_passes_test(lambda u: u.is_superuser)
def export_inactive_demands_csv(request):
    def get(self, request):
        # Получаем все заявки
        demands = Demand.objects.all()

        # Создаем текущую дату и время
        now = datetime.now()
        timestamp = now.strftime("%Y_%m_%d_%H:%M:%S")

        # Создаем объект HttpResponse с типом контента "text/csv"
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="inactive_demands_{timestamp}.csv"'

        # Создаем объект writer для записи данных в CSV
        writer = csv.writer(response)

        # Записываем заголовки столбцов
        writer.writerow(['Date', 'Email', 'First name', 'Surname', 'Patronymic', 'Phonenumber', 'Faculty',
                         'Course', 'Target', 'Stage', 'Result', 'Comment'])

        # Записываем данные заявок
        for demand in demands:
            user_profile = demand.user_profile
            writer.writerow([
                demand.date_created,
                user_profile.email if user_profile else "",  # Проверка на наличие user_profile
                user_profile.firstname if user_profile else "",
                user_profile.surname if user_profile else "",
                user_profile.patronymic if user_profile else "",
                user_profile.phonenumber if user_profile else "",
                user_profile.faculty if user_profile else "",
                user_profile.course if user_profile else "",
                demand.target,
                demand.stage,
                demand.result,
                demand.comment
            ])

        return response


@login_required
def my_demands(request):
    user = request.user
    demands = Demand.objects.filter(user_profile=user.userprofile)
    return render(request, 'my-demands.html', {'demands': demands})


# class ExportDemandsExcelView(View):
#     def get(self, request):
#         # Получаем все заявки
#         demands = Demand.objects.all()
#
#         # Создаем объект Workbook
#         workbook = Workbook()
#
#         # Получаем активный лист
#         sheet = workbook.active
#
#         # Записываем заголовки столбцов
#         sheet.append([ 'Salary', 'Faculty', 'Target', 'Stage', 'Result'])
#
#         # Записываем данные заявок
#         for demand in demands:
#             sheet.append([ demand.salary, demand.faculty, demand.target, demand.stage, demand.result])
#
#         # Создаем HttpResponse с типом контента "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         response['Content-Disposition'] = 'attachment; filename="demands.xlsx"'
#
#         # Сохраняем Workbook в HttpResponse
#         workbook.save(response)
#
#         return response


def error_403(request, exception):
    return render(request, '403.html', status=403)


def error_500(request):
    return render(request, '500.html', status=500)


def error_502(request):
    return render(request, '502.html', status=502)


def about_us(request):
    return render(request, 'about-us.html')


def for_student(request):
    return render(request, 'for-student.html')


def for_employer(request):
    return render(request, 'for-employer.html')


def admin_test(request):
    return render(request, 'admin/admin-template.html')


def contacts(request):
    return render(request, 'contacts.html')


def my_demands(request):
    # Получить заявки пользователя
    user = request.user
    demands = Demand.objects.filter(user_profile=user.id)

    # Передать заявки в контекст шаблона
    context = {
        'demands': demands
    }
    return render(request, 'my-demands.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_help(request):
    return render(request, 'admin-help.html')

def tos(request):
    return render(request, 'tos.html')

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Создание нового пользователя на основе данных из формы
            user = UserProfile.objects.create(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['email'],  # Используем email в качестве имени пользователя
                firstname=form.cleaned_data['firstname'],
                surname=form.cleaned_data['surname'],
                patronymic=form.cleaned_data['patronymic'],
                phonenumber=form.cleaned_data['phonenumber'],
                have_whatsapp=form.cleaned_data['have_whatsapp'],
                have_telegram=form.cleaned_data['have_telegram'],
                have_viber=form.cleaned_data['have_viber'],
                faculty=form.cleaned_data['faculty'],
                course=form.cleaned_data['course']
            )
            # Дополнительные действия, если необходимо
            # ...

            # Перенаправление пользователя после успешной регистрации
            return redirect(
                'profile')  # Замените 'registration_success' на URL-шаблон для страницы успешной регистрации
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


# @login_required
# def update_profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('/profile/')  # Перенаправляем пользователя на страницу профиля после сохранения
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     return render(request, 'update_profile.html', {'form': form})


def surveys(request):
    surveys = Survey.objects.all()
    return render(request, 'surveys.html', {'surveys': surveys})

def take_survey(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    return render(request, 'take_survey.html', {'survey': survey})


def create_survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            # Сохранение опроса, если данные формы действительны
            survey = form.save()
            return redirect('/index')
    else:
        # Если это GET-запрос, просто отобразите пустую форму
        form = SurveyForm()

    return render(request, 'create_survey.html', {'form': form})

def create_survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            # Сохранение опроса, если данные формы действительны
            survey = form.save()
            return redirect('/index')
    else:
        # Если это GET-запрос, просто отобразите пустую форму
        form = SurveyForm()

    return render(request, 'create_survey.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def edit_survey(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    survey_form = SurveyForm(instance=survey)
    question_form = QuestionForm()  # Initialize form for creating a new question
    edit_question_form = EditQuestionForm()  # Initialize form for editing an existing question
    # Получаем общее количество вопросов
    question_count = survey.question_set.count()

    if request.method == 'POST':
        if 'save_survey' in request.POST:
            survey_form = SurveyForm(request.POST, instance=survey)
            if survey_form.is_valid():
                survey_form.save()
        else:
            if 'edit_question_id' in request.POST:
                question_id = request.POST.get('edit_question_id')
                question = Question.objects.get(pk=question_id)
                edit_question_form = EditQuestionForm(request.POST, instance=question)
            elif 'add_question' in request.POST:  # Добавление нового вопроса
                question_form = QuestionForm(request.POST)
                if question_form.is_valid():
                    new_question = question_form.save(commit=False)
                    new_question.survey = survey
                    new_question.save()
                    return redirect('edit_survey', survey_id=survey_id)

            if edit_question_form.is_valid():
                edit_question = edit_question_form.save(commit=False)
                edit_question.survey = survey

                # Handle the checkbox value properly
                is_mandatory = request.POST.get('is_mandatory')
                if is_mandatory:
                    edit_question.is_mandatory = True
                else:
                    edit_question.is_mandatory = False

                edit_question.save()
                return redirect('edit_survey', survey_id=survey_id)

    questions = survey.question_set.all()

    return render(request, 'edit_survey.html', {
        'survey': survey,
        'survey_form': survey_form,
        'question_form': question_form,
        'edit_question_form': edit_question_form,
        'questions': questions,
        'question_count': question_count
    })
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)  # Проверяем, что пользователь - суперпользователь
def survey_master(request):
    surveys = Survey.objects.all()  # Получаем список всех опросов
    total_surveys = surveys.count()
    return render(request, 'survey-master.html', {'surveys': surveys, 'total_surveys': total_surveys})
def is_superuser(user):
    return user.is_superuser
@user_passes_test(is_superuser)
def delete_question(request, survey_id, question_id):
    # Получаем вопрос или вызываем 404 ошибку, если он не существует
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        # Удаление вопроса
        question.delete()
        return redirect('edit-survey', survey_id=survey_id)  # Используем survey_id

    # Возвращаем шаблон подтверждения удаления
    return render(request, 'delete-question.html', {'question': question})


from django.contrib.auth.decorators import login_required


@login_required
def take_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)

    if request.method == 'POST':
        for question in survey.question_set.all():
            answer_data = request.POST.getlist('question_' + str(question.id))

            if answer_data:
                # Создаем объект Answer для этого вопроса
                answer = Answer(question=question, user_profile=request.user)

                # Остальной код обработки ответов остается без изменений

                answer.save()

    return render(request, 'take-survey.html', {'survey': survey})

def survey_answers(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    users_with_answers = Answer.objects.filter(question__survey=survey).values('user_profile').distinct()
    users_and_answers = []

    for user_with_answer in users_with_answers:
        user_profile_id = user_with_answer['user_profile']
        user_profile = UserProfile.objects.get(pk=user_profile_id)
        users_and_answers.append({'user_profile': user_profile})

    return render(request, 'survey_answers.html', {'survey': survey, 'users_and_answers': users_and_answers})

def user_answers(request, user_id, survey_id):
    user_answers = Answer.objects.filter(user_profile=user_id, question__survey=survey_id)
    user_profile = user_answers.first().user_profile

    return render(request, 'user_answers.html', {'user_answers': user_answers, 'user_profile': user_profile})



#restapi
class UserProfileDetailView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer