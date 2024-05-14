from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelChoiceField
from django.views.generic import FormView
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, Demand, Survey, Question
from django.contrib.auth import get_user_model




class UserProfileEditForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    is_employer = forms.BooleanField(required=False)
    company = forms.CharField(required=False)
    faculty = forms.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'avatar', 'is_employer', 'company', 'faculty')


# class VacancyForm(forms.ModelForm):
#     User = get_user_model()
#     employer: ModelChoiceField = forms.ModelChoiceField(queryset=User.objects.filter(is_employer=True))
#     career_center_id = forms.IntegerField()
#
#     class Meta:
#         model = Vacancy
#         fields = (
#             'employer', 'career_center_id', 'title', 'short_description', 'main_description', 'salary', 'main_image',
#             'additional_images')


# class EmployerRegistrationForm(UserCreationForm):
#     avatar = forms.ImageField(required=False)
#     is_employer = forms.BooleanField(required=False)
#     company = forms.CharField(required=True)
#     faculty = forms.CharField(required=False)
#
#     class Meta:
#         model = UserProfile
#         fields = ('username', 'email', 'password1', 'password2', 'avatar', 'is_employer', 'company', 'faculty')
#
#
# class ApplicantRegistrationForm(UserCreationForm):
#     avatar = forms.ImageField(required=False)
#     is_employer = forms.BooleanField(required=False)
#     company = forms.CharField(required=False)
#     faculty = forms.CharField(required=True)
#
#     class Meta:
#         model = UserProfile
#         fields = ('username', 'email', 'password1', 'password2', 'avatar', 'is_employer', 'company', 'faculty')
#

# class AddDemandForm
class DemandForm(forms.ModelForm):
    have_whatsapp = forms.ModelChoiceField(queryset=UserProfile.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    have_viber = forms.ModelChoiceField(queryset=UserProfile.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    have_telegram = forms.ModelChoiceField(queryset=UserProfile.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    faculty = forms.ModelChoiceField(queryset=UserProfile.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Demand
        fields = ['have_whatsapp', 'have_viber', 'have_telegram', 'faculty', 'target', 'stage', 'result']


class AddDemandView(FormView):
    template_name = 'add_demand.html'
    form_class = DemandForm
    success_url = '/add_demand/'  # Укажите URL, на который будет перенаправлен пользователь после успешного сохранения формы

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['email', 'password', 'confirm_password', 'firstname', 'surname', 'patronymic', 'phonenumber',
                  'have_whatsapp', 'have_telegram', 'have_viber', 'faculty', 'course', 'recordbook', 'is_ended_study',
                  'year_of_ending']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Проверка соответствия пароля и его подтверждения
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Пароли не совпадают')

        return cleaned_data

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'short_description', 'description', 'description_after_passing']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'is_mandatory']

class EditQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'is_mandatory']
